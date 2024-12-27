import csv
import io
from pydantic import BaseModel
from sqlmodel import SQLModel, Session, not_, select
from src import base_categories
from src.dtos import ColumnMapper, MonthYear
from src.models import Account, Category, Transaction
from datetime import datetime
from decimal import Decimal
from typing import BinaryIO, Optional, Sequence
from sqlalchemy.sql import func
from sqlmodel.sql.expression import Select
from sqlalchemy.orm import joinedload

from src.services.categorization import CategorizationService


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
        exclude_from_analytics: bool = False,
    ) -> Transaction:
        transaction = Transaction(
            date=date,
            description=description,
            amount=amount,
            category_id=category_id,
            account_id=account_id,
            merchant_id=merchant_id,
            notes=notes,
            exclude_from_analytics=exclude_from_analytics,
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
            ).order_by(Transaction.date.desc())

        return self.session.exec(statement).all()

    def get_categories(self) -> Sequence[Category]:
        return self.session.exec(select(Category)).all()

    def get_category_analytics(self, month: Optional[MonthYear] = None) -> CategoryAnalyticsRespose:
        statement: Select = (
            select(Category.id, func.sum(Transaction.amount).label("total"))
            # Left join to include uncategorized transactions
            .join(Category, Category.id == Transaction.category_id, isouter=True)
            .where(not_(Transaction.exclude_from_analytics))
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
        headers, data = _get_file_data(file)
        _validate_headers(headers, column_mapper)

        transactions = data_to_transaction(data, account_id, column_mapper)
        for transaction in transactions:
            self.session.add(transaction)
        self.session.commit()


def _get_file_data(file: BinaryIO):
    file.seek(0)  # Ensure the file pointer is at the start
    reader = csv.DictReader(io.TextIOWrapper(file, encoding="utf-8"))
    reader.fieldnames = [field.lower() for field in reader.fieldnames]
    data = [row for row in reader]
    headers = reader.fieldnames
    return headers, data


def data_to_transaction(data, account_id: str, column_mapper: ColumnMapper):
    mapping_strategy = base_categories.category_mapping if column_mapper.category else base_categories.mapping
    cat_service = CategorizationService(mapping_strategy)

    transactions = []
    for row in data:
        # conver row["Date"] (eg: 07/09/2024) to a datetime object
        date = datetime.strptime(row[column_mapper.date], column_mapper.date_format)
        transaction = Transaction(
            date=date,
            description=row[column_mapper.description],
            amount=Decimal(row[column_mapper.amount]),
            account_id=account_id,
        )
        # Identify Payments, which need to be marked as Excluded
        if _is_payment(transaction.description, transaction.amount):
            transaction.exclude_from_analytics = True

        else:  # Categorize the transaction
            source_category = row.get(column_mapper.category)
            category_id = cat_service.categorize_transaction(transaction, source_category=source_category)
            transaction.category_id = category_id

        transactions.append(transaction)

    return transactions


def _is_payment(description: str, amount: Decimal) -> bool:
    """
    TODO: will likely need improvement to handle more cases
    """
    keywords = ["payment", "received"]
    return any(keyword in description.lower() for keyword in keywords) and amount < 0


def _validate_headers(headers, column_mapper: ColumnMapper):
    required_headers = [column_mapper.date, column_mapper.description, column_mapper.amount]
    if column_mapper.category:
        required_headers.append(column_mapper.category)

    missing_headers = set(required_headers) - set(headers)
    if missing_headers:
        raise ValueError(f"Missing headers: {missing_headers}")
