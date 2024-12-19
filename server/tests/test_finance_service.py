from sqlmodel import Session
from services.finances import FinanceService
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