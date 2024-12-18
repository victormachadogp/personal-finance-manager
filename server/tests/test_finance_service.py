import pytest
from sqlmodel import Session, create_engine, SQLModel
from services import FinanceService
from datetime import datetime
from decimal import Decimal

@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

def test_create_account(session):
    service = FinanceService(session)
    account = service.create_account(name="Test Account")
    assert account.id is not None
    assert account.name == "Test Account"

def test_create_category(session):
    service = FinanceService(session)
    category = service.create_category(title="Test Category", icon="bookmark")
    assert category.id is not None
    assert category.title == "Test Category"

def test_create_transaction(session):
    service = FinanceService(session)

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