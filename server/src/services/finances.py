from pydantic import BaseModel
from sqlmodel import SQLModel, Session, select
from src.models import Account, Category, Transaction
from datetime import datetime
from decimal import Decimal
from typing import Optional, Sequence

"""
TODO: Service is returning ORM objects, should return DTOs instead
"""


class CategoryAnalytics(SQLModel):
    category_id: str
    total: Decimal


class CategoryAnalyticsRespose(BaseModel):
    categories: list[CategoryAnalytics]
    total: Decimal


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

    def get_transactions(self) -> Sequence[Transaction]:
        return self.session.exec(select(Transaction)).all()

    def get_categories(self) -> Sequence[Category]:
        return self.session.exec(select(Category)).all()

    def get_category_analytics(self) -> CategoryAnalyticsRespose:
        from sqlalchemy.sql import func

        statement = (
            select(
                Category.id,  # Select the category title
                func.sum(Transaction.amount).label("total"),  # Sum of transaction amounts
            )
            .join(Category, Category.id == Transaction.category_id)  # Join Transaction and Category on category_id
            .group_by(Category.title)  # Group by category title
        )

        results = self.session.exec(statement).all()  # Execute the query

        # Convert the results to instances of CategoryAnalytics
        analytics = [CategoryAnalytics(category_id=row.id, total=row.total) for row in results]

        return CategoryAnalyticsRespose(categories=analytics, total=sum([a.total for a in analytics]))
