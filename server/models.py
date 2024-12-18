from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from datetime import datetime
# from enum import Enum
import shortuuid
from decimal import Decimal


def generate_id():
    return shortuuid.uuid()


class Category(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=generate_id, primary_key=True)
    title: str = Field(index=True)
    icon: str
    color: str = Field(default="#000000") 


class Merchant(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=generate_id, primary_key=True)
    name: str = Field(index=True)
    logo_icon: str


class Account(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=generate_id, primary_key=True)
    name: str = Field(index=True)
    # icon_logo: str


# class TransactionType(str, Enum):
#     debit = "debit"
#     credit = "credit"


class Transaction(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=generate_id, primary_key=True)
    date: datetime
    description: str
    amount: Decimal = Field(..., decimal_places=2)
    notes: Optional[str] = Field(default=None)
    category_id: int = Field(foreign_key="category.id")
    merchant_id: Optional[str] = Field(default=None, foreign_key="merchant.id")
    account_id: int = Field(foreign_key="account.id")
    # type: TransactionType
    # category: Category = Relationship(back_populates="transactions")
    # merchant: Optional[Merchant] = Relationship(back_populates="transactions")
    # account: Account = Relationship(back_populates="transactions")


# Adding relationships to Category, Merchant, and Account
# Category.transactions: List[Transaction] = Relationship(back_populates="category")
# Merchant.transactions: List[Transaction] = Relationship(back_populates="merchant")
# Account.transactions: List[Transaction] = Relationship(back_populates="account")
