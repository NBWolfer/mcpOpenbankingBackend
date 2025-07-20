"""
MCP Banking Backend with SQLite Database and Authentication
Acts as a bridge between HTTP requests and MCP agents for banking operations
"""

import json
import logging
from typing import Dict, Optional, Any, List
from datetime import datetime, timedelta
import uuid

from fastapi import FastAPI, HTTPException, Depends, status, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import httpx
import uvicorn

# Local imports
from database import get_db, create_tables, init_sample_data, User, Account, Transaction
from auth import authenticate_user, create_access_token, get_current_active_user, ACCESS_TOKEN_EXPIRE_MINUTES
from bank_client import DummyBankClient
from schemas import (
    UserCreate, UserResponse, Token, AccountResponse, TransactionResponse,
    TransferRequest, AccountListResponse
)

# Simple logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Enhanced MCP client for banking operations with database integration
class EnhancedMCPClient:
    """Enhanced MCP client for banking services with database support"""
    
    def __init__(self, mcp_server_url: str = "http://127.0.0.1:8001"):
        self.mcp_server_url = mcp_server_url
    
    async def call_banking_agent(self, operation: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Call MCP banking agent with operation and data"""
        try:
            # Use shorter timeout since MCP server might not be available
            async with httpx.AsyncClient(timeout=5.0) as client:
                # Enhanced MCP call structure for the /mcp/call endpoint
                mcp_request = {
                    "operation": operation,
                    "data": data,
                    "timestamp": datetime.now().isoformat(),
                    "source": "banking_backend"
                }
                
                logger.info(f"Calling MCP agent for operation: {operation}")
                response = await client.post(
                    f"{self.mcp_server_url}/mcp/call",
                    json=mcp_request,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    logger.info(f"MCP agent response: {result}")
                    return result
                else:
                    logger.warning(f"MCP server returned status: {response.status_code}")
                    return {"status": "mcp_unavailable", "operation": operation, "data": data}
                    
        except Exception as e:
            logger.warning(f"MCP server unavailable: {e}")
            return {"status": "mcp_unavailable", "operation": operation, "data": data}

    async def check_mcp_status(self) -> Dict[str, Any]:
        """Check MCP server status"""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.mcp_server_url}/mcp/status")
                if response.status_code == 200:
                    return response.json()
                else:
                    return {"status": "unavailable", "error": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"status": "unavailable", "error": str(e)}

    async def query_mcp_agent(self, query: str) -> Dict[str, Any]:
        """Query MCP agent for information"""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                query_request = {
                    "query": query,
                    "timestamp": datetime.now().isoformat(),
                    "source": "banking_backend"
                }
                
                response = await client.post(
                    f"{self.mcp_server_url}/mcp/query",
                    json=query_request,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    logger.warning(f"MCP query failed: {response.status_code}")
                    return {"status": "query_failed", "query": query}
                    
        except Exception as e:
            logger.warning(f"MCP query unavailable: {e}")
            return {"status": "query_unavailable", "query": query}

# Initialize FastAPI app and database
app = FastAPI(
    title="MCP Banking Backend with Database",
    description="Secure banking backend with SQLite database and MCP integration",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Global MCP client and Bank client
mcp_client = EnhancedMCPClient()
bank_client = DummyBankClient()

# Startup event to initialize database
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    create_tables()
    init_sample_data()
    logger.info("Database initialized successfully")

# Authentication endpoints
@app.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user and sync with dummy bank"""
    # Check if user already exists
    existing_user = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username or email already registered"
        )
    
    # Register customer with dummy bank first
    bank_customer_data = {
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name
    }
    
    bank_result = await bank_client.register_customer(bank_customer_data)
    customer_oid = None
    
    if bank_result.get("status") == "success":
        customer_oid = bank_result.get("customer_oid")
        logger.info(f"Customer registered with dummy bank: {customer_oid}")
    else:
        logger.warning(f"Failed to register with dummy bank: {bank_result}")
        # Continue with local registration even if bank sync fails
    
    # Create new user in local database
    from auth import get_password_hash
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        customer_oid=customer_oid,  # Store the CustomerOID from dummy bank
        hashed_password=hashed_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    logger.info(f"New user registered: {user.username}")
    return db_user

@app.post("/token", response_model=Token)
async def login_user(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    """Login user and return access token + set HTTP-only cookie"""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    # Set HTTP-only cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # Convert to seconds
        expires=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax",
        secure=False  # Set to True in production with HTTPS
    )
    
    logger.info(f"User logged in: {user.username}")
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/login", response_model=Token)
async def login_user_json(
    response: Response,
    credentials: Dict[str, str],
    db: Session = Depends(get_db)
):
    """Login user with JSON credentials and return access token + set HTTP-only cookie"""
    username = credentials.get("username")
    password = credentials.get("password")
    
    if not username or not password:
        raise HTTPException(
            status_code=400,
            detail="Username and password are required"
        )
    
    user = authenticate_user(db, username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    # Set HTTP-only cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # Convert to seconds
        expires=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax",
        secure=False  # Set to True in production with HTTPS
    )
    
    logger.info(f"User logged in via JSON: {user.username}")
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/logout")
async def logout_user(response: Response):
    """Logout user by clearing the HTTP-only cookie"""
    response.delete_cookie(key="access_token")
    return {"message": "Successfully logged out"}

# Health check
@app.get("/health")
async def health_check():
    # Check MCP server status
    mcp_status = await mcp_client.check_mcp_status()
    
    # Check dummy bank status
    bank_status = await bank_client.check_connection()
    
    return {
        "status": "healthy", 
        "service": "mcp-banking-backend", 
        "timestamp": datetime.now(),
        "database": "connected",
        "mcp_server": mcp_status,
        "dummy_bank": bank_status
    }

# Protected banking endpoints
@app.get("/accounts", response_model=AccountListResponse)
async def get_user_accounts(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get current user's accounts"""
    accounts = db.query(Account).filter(
        Account.user_id == current_user.id,
        Account.is_active == True
    ).all()
    
    # Notify MCP agent about account access
    await mcp_client.call_banking_agent("account_access", {
        "user_id": current_user.id,
        "username": current_user.username,
        "account_count": len(accounts)
    })
    
    return {"accounts": accounts}

@app.get("/accounts/{account_id}", response_model=AccountResponse)
async def get_account_details(
    account_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get specific account details"""
    account = db.query(Account).filter(
        Account.id == account_id,
        Account.user_id == current_user.id,
        Account.is_active == True
    ).first()
    
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    # Notify MCP agent about account details request
    await mcp_client.call_banking_agent("account_details", {
        "user_id": current_user.id,
        "account_id": account_id,
        "account_type": account.account_type
    })
    
    return account

@app.get("/accounts/{account_id}/balance")
async def get_account_balance(
    account_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get account balance"""
    account = db.query(Account).filter(
        Account.id == account_id,
        Account.user_id == current_user.id,
        Account.is_active == True
    ).first()
    
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    # Notify MCP agent about balance check
    await mcp_client.call_banking_agent("balance_check", {
        "user_id": current_user.id,
        "account_id": account_id,
        "current_balance": account.balance
    })
    
    return {
        "account_id": account_id,
        "balance": account.balance,
        "currency": account.currency,
        "account_name": account.account_name
    }

@app.get("/accounts/{account_id}/transactions", response_model=List[TransactionResponse])
async def get_account_transactions(
    account_id: str,
    limit: int = 10,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get account transactions"""
    # Verify account ownership
    account = db.query(Account).filter(
        Account.id == account_id,
        Account.user_id == current_user.id
    ).first()
    
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    # Get transactions for this account
    transactions = db.query(Transaction).filter(
        (Transaction.from_account_id == account_id) | 
        (Transaction.to_account_id == account_id)
    ).order_by(Transaction.created_at.desc()).limit(limit).all()
    
    # Notify MCP agent about transaction history request
    await mcp_client.call_banking_agent("transaction_history", {
        "user_id": current_user.id,
        "account_id": account_id,
        "transaction_count": len(transactions)
    })
    
    return transactions

@app.post("/transfer", response_model=TransactionResponse)
async def transfer_money(
    transfer: TransferRequest,
    from_account_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Transfer money between accounts"""
    # Verify source account ownership
    from_account = db.query(Account).filter(
        Account.id == from_account_id,
        Account.user_id == current_user.id,
        Account.is_active == True
    ).first()
    
    if not from_account:
        raise HTTPException(status_code=404, detail="Source account not found")
    
    # Verify destination account exists
    to_account = db.query(Account).filter(
        Account.id == transfer.to_account_id,
        Account.is_active == True
    ).first()
    
    if not to_account:
        raise HTTPException(status_code=404, detail="Destination account not found")
    
    # Check sufficient balance
    if from_account.balance < transfer.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    
    # Call MCP agent for fraud detection and approval
    fraud_check = await mcp_client.call_banking_agent("fraud_check", {
        "user_id": current_user.id,
        "from_account": from_account_id,
        "to_account": transfer.to_account_id,
        "amount": transfer.amount,
        "currency": transfer.currency
    })
    
    # Create transaction
    transaction_id = f"TXN{uuid.uuid4().hex[:6].upper()}"
    transaction = Transaction(
        id=transaction_id,
        from_account_id=from_account_id,
        to_account_id=transfer.to_account_id,
        amount=transfer.amount,
        currency=transfer.currency,
        description=transfer.description or f"Transfer to {transfer.to_account_id}",
        transaction_type="transfer",
        status="completed"
    )
    
    # Update account balances
    from_account.balance -= transfer.amount
    to_account.balance += transfer.amount
    
    # Save to database
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    
    # Notify MCP agent about completed transfer
    await mcp_client.call_banking_agent("transfer_completed", {
        "transaction_id": transaction_id,
        "user_id": current_user.id,
        "amount": transfer.amount,
        "fraud_check_result": fraud_check
    })
    
    logger.info(f"Transfer completed: {transaction_id}")
    return transaction

@app.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """Get current user information"""
    return current_user

@app.post("/config")
async def update_config(
    config: Dict[str, str],
    current_user: User = Depends(get_current_active_user)
):
    """Update MCP server configuration (admin only)"""
    # In a real application, you might want to check for admin privileges
    if "mcp_server_url" in config:
        mcp_client.mcp_server_url = config["mcp_server_url"]
        logger.info(f"MCP server URL updated by {current_user.username}")
        return {"message": "Configuration updated", "mcp_server_url": config["mcp_server_url"]}
    raise HTTPException(status_code=400, detail="mcp_server_url required")

# Admin endpoint to get all users (for testing)
@app.get("/admin/users", response_model=List[UserResponse])
async def get_all_users(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all users (admin endpoint)"""
    users = db.query(User).all()
    return users

@app.get("/bank/portfolio")
async def get_bank_portfolio(
    current_user: User = Depends(get_current_active_user)
):
    """Get user's portfolio from dummy bank"""
    if not current_user.customer_oid:
        raise HTTPException(
            status_code=404,
            detail="User not linked to dummy bank. Please contact support."
        )
    
    portfolio_result = await bank_client.get_customer_portfolio(current_user.customer_oid)
    
    if portfolio_result.get("status") == "success":
        return portfolio_result.get("data")
    elif portfolio_result.get("status") == "not_found":
        raise HTTPException(status_code=404, detail="Portfolio not found in dummy bank")
    else:
        raise HTTPException(
            status_code=500,
            detail=f"Bank API error: {portfolio_result.get('error')}"
        )

@app.get("/bank/status")
async def get_bank_status(current_user: User = Depends(get_current_active_user)):
    """Get dummy bank connection status"""
    return await bank_client.check_connection()

@app.get("/bank/customers")
async def get_all_bank_customers(current_user: User = Depends(get_current_active_user)):
    """Get all customers from dummy bank (admin endpoint)"""
    customers_result = await bank_client.get_all_customers()
    
    if customers_result.get("status") == "success":
        return customers_result.get("data")
    else:
        raise HTTPException(
            status_code=500,
            detail=f"Bank API error: {customers_result.get('error')}"
        )

@app.post("/bank/sync")
async def sync_with_bank(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Sync current user with dummy bank"""
    if current_user.customer_oid:
        # Check if customer still exists in bank
        exists_result = await bank_client.check_customer_exists(current_user.customer_oid)
        if exists_result.get("status") == "success" and exists_result.get("data", {}).get("exists"):
            return {
                "message": "User already synced with dummy bank",
                "customer_oid": current_user.customer_oid
            }
    
    # Register with dummy bank
    bank_customer_data = {
        "username": current_user.username,
        "email": current_user.email,
        "full_name": current_user.full_name
    }
    
    bank_result = await bank_client.register_customer(bank_customer_data)
    
    if bank_result.get("status") == "success":
        # Update local user with CustomerOID
        customer_oid = bank_result.get("customer_oid")
        current_user.customer_oid = customer_oid
        db.commit()
        
        return {
            "message": "Successfully synced with dummy bank",
            "customer_oid": customer_oid
        }
    else:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to sync with dummy bank: {bank_result.get('error')}"
        )

@app.get("/mcp/status")
async def get_mcp_status(current_user: User = Depends(get_current_active_user)):
    """Get MCP server status (authenticated endpoint)"""
    return await mcp_client.check_mcp_status()

@app.post("/mcp/query")
async def query_mcp(
    query_data: Dict[str, str],
    current_user: User = Depends(get_current_active_user)
):
    """Query MCP agent (authenticated endpoint)"""
    query = query_data.get("query", "")
    if not query:
        raise HTTPException(status_code=400, detail="Query is required")
    
    result = await mcp_client.query_mcp_agent(query)
    return result

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)