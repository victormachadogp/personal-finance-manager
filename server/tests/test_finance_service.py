import io
from typing import BinaryIO
import pytest
from sqlmodel import Session
from src.dtos import ColumnMapper, MonthYear
from src.models import Account
from src.services.finances import FinanceService
from datetime import datetime
from decimal import Decimal


def test_create_account(db_session: Session):
    service = FinanceService(db_session)
    account = service.create_account(name="Test Account", currency_id="gbp")
    assert account.id is not None
    assert account.name == "Test Account"


def test_create_category(db_session: Session):
    service = FinanceService(db_session)
    category = service.create_category(title="Test Category", icon="bookmark")
    assert category.id is not None
    assert category.title == "Test Category"


def test_create_transaction(db_session: Session, account: Account):
    service = FinanceService(db_session)

    category = service.create_category(title="Test Category", icon="bookmark")

    transaction = service.create_transaction(
        date=datetime.now(),
        description="Test Transaction",
        amount=Decimal("100.00"),
        category_id=category.id,
        account_id=account.id,
    )

    assert transaction.id is not None
    assert transaction.description == "Test Transaction"


def test_get_transactions(db_session: Session, account: Account):
    service = FinanceService(db_session)

    """GIVEN a set of transactions"""
    date = datetime.now()
    acc_id = account.id
    service.create_transaction(date=date, description="Test 1", amount=Decimal("100.00"), account_id=acc_id)
    service.create_transaction(date=date, description="Test 2", amount=Decimal("50.00"), account_id=acc_id)

    """WHEN fetching transactions"""
    transactions = service.get_transactions()

    """THEN the response should contain the transactions"""
    assert len(transactions) == 2


def test_get_transactions_by_month(db_session: Session, account: Account):
    service = FinanceService(db_session)

    """GIVEN a set of transactions"""
    acc_id = account.id
    jan2025 = datetime(2025, 1, 1)
    service.create_transaction(date=jan2025, description="Test 1", amount=Decimal("100.00"), account_id=acc_id)
    service.create_transaction(date=jan2025, description="Test 2", amount=Decimal("50.00"), account_id=acc_id)
    dec2024 = datetime(2024, 12, 1)
    service.create_transaction(date=dec2024, description="Test 2", amount=Decimal("50.00"), account_id=acc_id)

    """WHEN fetching transactions"""
    transactions = service.get_transactions(month=MonthYear(year=2025, month=1))

    """THEN the response should contain the transactions"""
    assert len(transactions) == 2
    assert transactions[0].date == jan2025
    assert transactions[1].date == jan2025


def test_get_category_analytics(db_session: Session, account: Account):
    service = FinanceService(db_session)

    """GIVEN a set of transactions"""
    cat1 = service.create_category(title="Cat1", icon="bookmark")
    cat2 = service.create_category(title="Cat2", icon="bookmark")

    date = datetime.now()
    acc_id = account.id
    service.create_transaction(  # Category 1
        date=date, description="", amount=Decimal("100.00"), category_id=cat1.id, account_id=acc_id
    )
    service.create_transaction(  # Category 1
        date=date, description="", amount=Decimal("50.00"), category_id=cat1.id, account_id=acc_id
    )
    service.create_transaction(  # Category 2
        date=date, description="", amount=Decimal("100.00"), category_id=cat2.id, account_id=acc_id
    )

    service.create_transaction(  # No Category
        date=date, description="", amount=Decimal("50.00"), category_id=None, account_id=acc_id
    )

    """WHEN fetching category analytics"""
    res = service.get_category_analytics()

    """THEN the response should contain the total amount"""
    assert res.total == Decimal("300.00")
    assert len(res.categories) == 3

    # Check the category totals (categories are sorted by total descending)
    assert res.categories[0].id == cat1.id
    assert res.categories[0].total == Decimal("150.00")

    assert res.categories[1].id == cat2.id
    assert res.categories[1].total == Decimal("100.00")

    assert res.categories[2].id is None
    assert res.categories[2].total == Decimal("50.00")


def test_get_category_analytics_by_month(db_session: Session, account: Account):
    service = FinanceService(db_session)

    """GIVEN a set of transactions"""
    cat1 = service.create_category(title="Cat1", icon="bookmark")
    cat2 = service.create_category(title="Cat2", icon="bookmark")

    jan2025 = datetime(2025, 1, 1)
    acc_id = account.id
    service.create_transaction(  # Category 1
        date=jan2025, description="", amount=Decimal("100.00"), category_id=cat1.id, account_id=acc_id
    )
    service.create_transaction(  # Category 2
        date=jan2025, description="", amount=Decimal("100.00"), category_id=cat2.id, account_id=acc_id
    )

    service.create_transaction(  # No Category
        date=jan2025, description="", amount=Decimal("50.00"), category_id=None, account_id=acc_id
    )
    dec2024 = datetime(2024, 12, 1)  # Should not be included
    service.create_transaction(  # Category 1
        date=dec2024, description="", amount=Decimal("500.00"), category_id=cat1.id, account_id=acc_id
    )

    """WHEN fetching category analytics"""
    res = service.get_category_analytics(month=MonthYear(year=2025, month=1))

    """THEN the response should contain the total amount"""
    assert res.total == Decimal("250.00")
    assert len(res.categories) == 3


def test_file_import(db_session: Session, csv_file: BinaryIO, account: Account):
    service = FinanceService(db_session)
    transactions = service.get_transactions()
    assert len(transactions) == 0

    """GIVEN a CSV file with transactions"""
    column_mapper = ColumnMapper(date="Date", description="Description", amount="Amount", date_format="%Y-%m-%d")

    """WHEN importing the CSV file"""
    service.import_csv(file=csv_file, account_id=account.id, column_mapper=column_mapper)

    """THEN the transactions should be imported"""
    transactions = service.get_transactions()
    assert len(transactions) == 2
