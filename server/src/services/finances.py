import csv
import io
from pydantic import BaseModel
from sqlmodel import SQLModel, Session, select
from src.dtos import ColumnMapper, MonthYear
from src.models import Account, Category, Transaction
from datetime import datetime
from decimal import Decimal
from typing import BinaryIO, Optional, Sequence
from sqlalchemy.sql import func
from sqlmodel.sql.expression import Select
from sqlalchemy.orm import joinedload

from src.tools import data_to_transaction

"""
TODO: Service is returning ORM objects, should return DTOs instead
"""


class CategoryAnalytics(SQLModel):
    id: Optional[str]  # None for uncategorized transactions
    total: Decimal


class CategoryAnalyticsRespose(BaseModel):
    categories: list[CategoryAnalytics]
    total: Decimal


class FinanceService:
    def __init__(self, session: Session):
        self.session = session

    def create_account(self, name: str, currency_id: str) -> Account:
        account = Account(name=name, currency_id=currency_id)
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
        *,
        date: datetime,
        description: str,
        amount: Decimal,
        category_id: Optional[str] = None,
        account_id: str,
        merchant_id: Optional[str] = None,
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

    def get_transactions(self, month: Optional[MonthYear] = None) -> Sequence[Transaction]:
        statement = select(Transaction)

        # Filter by month if provided
        if month:
            statement = statement.where(
                func.extract("year", Transaction.date) == month.year,
                func.extract("month", Transaction.date) == month.month,
            )

        return self.session.exec(statement).all()

    def get_categories(self) -> Sequence[Category]:
        return self.session.exec(select(Category)).all()

    def get_category_analytics(self, month: Optional[MonthYear] = None) -> CategoryAnalyticsRespose:
        statement: Select = (
            select(Category.id, func.sum(Transaction.amount).label("total"))
            # Left join to include uncategorized transactions
            .join(Category, Category.id == Transaction.category_id, isouter=True)
            .group_by(Category.id)
            .order_by(func.sum(Transaction.amount).desc())
        )

        # Filter by month if provided
        if month:
            statement = statement.where(
                func.extract("year", Transaction.date) == month.year,
                func.extract("month", Transaction.date) == month.month,
            )

        results = self.session.exec(statement).all()  # Execute the query

        # Convert the results to instances of CategoryAnalytics
        analytics = [CategoryAnalytics(id=row.id, total=row.total) for row in results]

        return CategoryAnalyticsRespose(categories=analytics, total=sum([a.total for a in analytics]))

    def get_accounts(self) -> Sequence[Account]:
        # join account with currency to get currency details
        statement = select(Account).options(joinedload(Account.currency)).order_by(Account.name)
        return self.session.exec(statement).all()

    def import_csv(self, file: BinaryIO, account_id: str, column_mapper: ColumnMapper):
        
        data = self._get_file_data(file)
        transactions = data_to_transaction(data, account_id, column_mapper)
        for transaction in transactions:
            self.session.add(transaction)
        self.session.commit()

    def _get_file_data(self, file: BinaryIO):
        file.seek(0)  # Ensure the file pointer is at the start
        reader = csv.DictReader(io.TextIOWrapper(file, encoding='utf-8'))
        return [row for row in reader]
