"""
Database models and configuration for MCP Banking Backend
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

# Database configuration
SQLITE_DATABASE_URL = "sqlite:///./banking.db"

engine = create_engine(
    SQLITE_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Database Models
class User(Base):
    """User model for authentication"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    customer_oid = Column(String, unique=True, index=True, nullable=True)  # UUID from dummy bank
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to accounts
    accounts = relationship("Account", back_populates="owner")

class Account(Base):
    """Account model"""
    __tablename__ = "accounts"
    
    id = Column(String, primary_key=True, index=True)  # Account ID like ACC001
    account_name = Column(String, nullable=False)
    account_type = Column(String, nullable=False)  # checking, savings, credit
    balance = Column(Float, default=0.0)
    currency = Column(String, default="USD")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Foreign key to user
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="accounts")
    
    # Relationship to transactions
    sent_transactions = relationship("Transaction", foreign_keys="Transaction.from_account_id", back_populates="from_account")
    received_transactions = relationship("Transaction", foreign_keys="Transaction.to_account_id", back_populates="to_account")

class Transaction(Base):
    """Transaction model"""
    __tablename__ = "transactions"
    
    id = Column(String, primary_key=True, index=True)  # Transaction ID like TXN001
    from_account_id = Column(String, ForeignKey("accounts.id"))
    to_account_id = Column(String, ForeignKey("accounts.id"))
    amount = Column(Float, nullable=False)
    currency = Column(String, default="USD")
    description = Column(String)
    transaction_type = Column(String, nullable=False)  # transfer, deposit, withdrawal
    status = Column(String, default="pending")  # pending, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    from_account = relationship("Account", foreign_keys=[from_account_id], back_populates="sent_transactions")
    to_account = relationship("Account", foreign_keys=[to_account_id], back_populates="received_transactions")

# Database dependency
def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables
def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)

# Initialize database with sample data
def init_sample_data():
    """Initialize database with sample data"""
    from auth import get_password_hash
    import uuid
    import asyncio
    import httpx
    
    async def register_with_dummy_bank(name: str) -> str:
        """Register customer with dummy bank and return CustomerOID"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    "http://127.0.0.1:3000/register-customer",
                    json={"name": name},
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code in [200, 201]:
                    result = response.json()
                    return result.get("customer_oid")
                else:
                    print(f"Failed to register {name} with dummy bank: {response.status_code}")
                    return None
        except Exception as e:
            print(f"Error registering {name} with dummy bank: {e}")
            return None
    
    async def init_data_async():
        """Async function to initialize data with dummy bank integration"""
        db = SessionLocal()
        try:
            # Check if data already exists
            if db.query(User).first():
                print("Sample data already exists, skipping initialization")
                return
            
            print("Initializing sample data with dummy bank integration...")
            
            # Register sample users with dummy bank and get CustomerOIDs
            john_customer_oid = await register_with_dummy_bank("John Doe")
            jane_customer_oid = await register_with_dummy_bank("Jane Smith")
            
            # Create sample users with CustomerOIDs from dummy bank
            user1 = User(
                username="john_doe",
                email="john@example.com",
                hashed_password=get_password_hash("password123"),
                full_name="John Doe",
                customer_oid=john_customer_oid
            )
            user2 = User(
                username="jane_smith",
                email="jane@example.com", 
                hashed_password=get_password_hash("password123"),
                full_name="Jane Smith",
                customer_oid=jane_customer_oid
            )
            
            db.add(user1)
            db.add(user2)
            db.commit()
            db.refresh(user1)
            db.refresh(user2)
            
            print(f"Created users - John: {john_customer_oid}, Jane: {jane_customer_oid}")
            
            # Create sample accounts
            accounts = [
                Account(id="ACC001", account_name="John's Checking", account_type="checking", 
                       balance=5000.0, user_id=user1.id),
                Account(id="ACC002", account_name="John's Savings", account_type="savings", 
                       balance=15000.0, user_id=user1.id),
                Account(id="ACC003", account_name="Jane's Checking", account_type="checking", 
                       balance=3000.0, user_id=user2.id),
                Account(id="ACC004", account_name="Jane's Savings", account_type="savings", 
                       balance=8000.0, user_id=user2.id),
            ]
            
            for account in accounts:
                db.add(account)
            
            db.commit()
            
            # Create sample transactions
            transactions = [
                Transaction(id="TXN001", from_account_id="ACC001", amount=50.0, 
                           description="ATM Withdrawal", transaction_type="withdrawal", status="completed"),
                Transaction(id="TXN002", to_account_id="ACC001", amount=1000.0, 
                           description="Salary Deposit", transaction_type="deposit", status="completed"),
                Transaction(id="TXN003", from_account_id="ACC001", to_account_id="ACC003", 
                           amount=200.0, description="Transfer to Jane", transaction_type="transfer", status="completed"),
            ]
            
            for transaction in transactions:
                db.add(transaction)
            
            db.commit()
            print("Sample data initialized successfully with dummy bank integration")
            
        except Exception as e:
            print(f"Error initializing sample data: {e}")
            db.rollback()
        finally:
            db.close()
    
    # Run the async initialization
    try:
        asyncio.run(init_data_async())
    except RuntimeError:
        # If we're already in an async context, use current loop
        import threading
        def run_in_thread():
            asyncio.run(init_data_async())
        
        thread = threading.Thread(target=run_in_thread)
        thread.start()
        thread.join()
