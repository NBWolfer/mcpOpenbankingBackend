from fastapi import FastAPI
from fastapi.security import OAuth2PasswordRequestForm
import httpx

from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from typing import Dict, List

import uvicorn
from database import User, Account, Transaction
from schemas import UserCreate, UserResponse, Token, AccountListResponse, AccountResponse, TransactionResponse
from database import get_db, create_tables, init_sample_data
from auth import authenticate_user, create_access_token, get_current_active_user, ACCESS_TOKEN_EXPIRE_MINUTES
from bank_client import DummyBankClient
from logging import getLogger

logger = getLogger(__name__)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3001", # React uygulamanızın çalıştığı port
    "http://localhost:3000", # Eğer başka bir port kullanıyorsanız buraya ekleyin
    "http://localhost:8001", # Eğer başka bir port kullanıyorsanız buraya ekleyin
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # veya spesifik olarak ["GET", "POST"]
    allow_headers=["*"],
)
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
    
    return transactions


@app.post("/mcp/query")
async def query_mcp(
    query_data: Dict[str, str],
    current_user: User = Depends(get_current_active_user)
):
    """Query MCP agent (authenticated endpoint)"""
    query = query_data.get("query", "")
    if not query:
        raise HTTPException(status_code=400, detail="Query is required")

    print(f"Received query from user {current_user.username}: {query}")

    # Define a longer timeout for this specific request
    timeout_config = httpx.Timeout(600.0, connect=5.0)

    try:
        async with httpx.AsyncClient(timeout=timeout_config) as client:
            response = await client.post(
                "http://localhost:8001/master-agent",
                json={"query": query, "oid": current_user.customer_oid}
            )

            # Raise an exception for bad status codes (4xx or 5xx)
            response.raise_for_status()

            # Return the JSON payload from the response
            return response.json()

    except httpx.ReadTimeout:
        raise HTTPException(
            status_code=504, # Gateway Timeout
            detail="The request to the agent timed out. Please try again later."
        )
    except httpx.RequestError as exc:
        # Catch other potential request errors (e.g., connection refused)
        raise HTTPException(
            status_code=503, # Service Unavailable
            detail=f"An error occurred while communicating with the agent: {exc}"
        )
        
@app.get("/me")
async def get_current_user(
    current_user: User = Depends(get_current_active_user)
):
    
    return current_user.customer_oid
        
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)