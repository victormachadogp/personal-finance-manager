import pytest
from sqlmodel import Session, create_engine, SQLModel

from src.models import Account
from src.services.finances import FinanceService


@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture
def account(db_session: Session) -> Account:
    service = FinanceService(db_session)
    account = service.create_account(name="Test Account")
    return account
