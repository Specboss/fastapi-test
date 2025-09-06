import enum
import uuid

from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.db import Base


class Role(str, enum.Enum):
    user = "user"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    role = Column(Enum(Role), default=Role.user, nullable=False)

    accounts = relationship("Account", back_populates="owner", cascade="all, delete-orphan")


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    balance = Column(Numeric(12, 2), default=0, nullable=False)

    owner = relationship("User", back_populates="accounts")


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(UUID(as_uuid=True), unique=True, nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)

    __table_args__ = (UniqueConstraint('transaction_id', name='uq_transaction_id'),)
