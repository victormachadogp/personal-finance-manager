from sqlmodel import Session
from src.models import Account
from src.services.finances import FinanceService
from datetime import datetime
from decimal import Decimal


def test_create_account(db_session: Session):
    service = FinanceService(db_session)
    account = service.create_account(name="Test Account")
    assert account.id is not None
    assert account.name == "Test Account"


def test_create_category(db_session: Session):
    service = FinanceService(db_session)
    category = service.create_category(title="Test Category", icon="bookmark")
    assert category.id is not None
    assert category.title == "Test Category"


def test_create_transaction(db_session: Session):
    service = FinanceService(db_session)

    account = service.create_account(name="Test Account")
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
