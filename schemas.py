"""
Pydantic schemas for request/response models
"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    customer_oid: Optional[str] = None
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Account schemas
class AccountBase(BaseModel):
    account_name: str
    account_type: str
    currency: str = "USD"

class AccountCreate(AccountBase):
    pass

class AccountResponse(AccountBase):
    id: str
    balance: float
    is_active: bool
    created_at: datetime
    user_id: int
    
    class Config:
        from_attributes = True

# Transaction schemas
class TransactionBase(BaseModel):
    amount: float
    currency: str = "USD"
    description: Optional[str] = None

class TransferRequest(TransactionBase):
    to_account_id: str

class TransactionResponse(TransactionBase):
    id: str
    from_account_id: Optional[str]
    to_account_id: Optional[str]
    transaction_type: str
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# Banking request schemas
class BalanceRequest(BaseModel):
    currency: str = "USD"

class AccountListResponse(BaseModel):
    accounts: List[AccountResponse]
