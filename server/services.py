from sqlmodel import Session
from models import Account, Category, Transaction
from datetime import datetime
from decimal import Decimal
from typing import Optional

"""
TODO: Service is returning ORM objects, should return DTOs instead
"""


class FinanceService:
    def __init__(self, session: Session):
        self.session = session

    def create_account(self, name: str) -> Account:
        account = Account(name=name)
        self.session.add(account)
        self.session.commit()
        self.session.refresh(account)
        return account

    def create_category(self, title: str, icon: str, color: Optional[str] = None) -> Category:
        category = Category(title=title, icon=icon, color=color)
        self.session.add(category)
        self.session.commit()
        self.session.refresh(category)
        return category

    def create_transaction(
        self,
        date: datetime,
        description: str,
        amount: Decimal,
        category_id: int,
        account_id: int,
        merchant_id: Optional[int] = None,
        notes: Optional[str] = None,
    ) -> Transaction:
        transaction = Transaction(
            date=date,
            description=description,
            amount=amount,
            category_id=category_id,
            account_id=account_id,
            merchant_id=merchant_id,
            notes=notes,
        )
        self.session.add(transaction)
        self.session.commit()
        self.session.refresh(transaction)
        return transaction
