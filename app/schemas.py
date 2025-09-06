from uuid import UUID
from decimal import Decimal
from typing import Optional, List

from pydantic import BaseModel, EmailStr

from app.models import Role


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    role: Optional[str] = "user"


class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str] = None
    role: Role

    class Config:
        from_attributes = True


class AccountRead(BaseModel):
    id: int
    balance: Decimal

    class Config:
        from_attributes = True


class PaymentRead(BaseModel):
    transaction_id: UUID
    account_id: int
    user_id: int
    amount: Decimal

    class Config:
        from_attributes = True
