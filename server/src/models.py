from sqlmodel import Field, Relationship, SQLModel
from typing import Optional
from datetime import datetime

# from enum import Enum
import shortuuid
from decimal import Decimal


def generate_id():
    return shortuuid.uuid()


class Category(SQLModel, table=True):
    id: str = Field(default_factory=generate_id, primary_key=True)
    title: str = Field(index=True)
    icon: str
    color: str = Field(default="#000000")


class Merchant(SQLModel, table=True):
    id: str = Field(default_factory=generate_id, primary_key=True)
    name: str = Field(index=True)
    logo_icon: str


class Currency(SQLModel, table=True):
    id: str = Field(..., primary_key=True)
    name: str = Field(index=True)
    code: str
    symbol: str

    accounts: list["Account"] = Relationship(back_populates="currency")


class Account(SQLModel, table=True):
    id: str = Field(default_factory=generate_id, primary_key=True)
    name: str = Field(index=True)
    currency_id: str = Field(foreign_key="currency.id")

    currency: Currency = Relationship(back_populates="accounts")


# class TransactionType(str, Enum):
#     debit = "debit"
#     credit = "credit"


class Transaction(SQLModel, table=True):
    id: str = Field(default_factory=generate_id, primary_key=True)
    date: datetime
    description: str
    amount: Decimal = Field(..., decimal_places=2)
    notes: Optional[str] = Field(default=None)
    category_id: Optional[str] = Field(default=None, foreign_key="category.id")
    merchant_id: Optional[str] = Field(default=None, foreign_key="merchant.id")
    account_id: str = Field(foreign_key="account.id")
    exclude_from_analytics: bool = Field(default=False)  # Stop it from being counted towards your spending (e.g. transfers between accounts)

    # type_: TransactionType
    # category: Category = Relationship(back_populates="transactions")
    # merchant: Optional[Merchant] = Relationship(back_populates="transactions")
    # account: Account = Relationship(back_populates="transactions")


# Adding relationships to Category, Merchant, and Account
# Category.transactions: List[Transaction] = Relationship(back_populates="category")
# Merchant.transactions: List[Transaction] = Relationship(back_populates="merchant")
# Account.transactions: List[Transaction] = Relationship(back_populates="account")
