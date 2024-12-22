import io
import os
from typing import BinaryIO, Iterator
import pytest
from sqlalchemy import Engine
from sqlmodel import Session, create_engine, SQLModel
from fastapi.testclient import TestClient

from src import database, dependencies
from src.models import Account
from src.services.finances import FinanceService


@pytest.fixture
def engine() -> Iterator[Engine]:
    test_db = "test.db"
    # Remove the SQLite database file if it exists
    if os.path.exists(test_db):
        os.remove(test_db)

    engine = create_engine(f"sqlite:///{test_db}")
    SQLModel.metadata.create_all(engine)
    yield engine

    # Teardown: Remove the SQLite database file
    if os.path.exists(test_db):
        os.remove(test_db)


@pytest.fixture
def db_session(engine: Engine):
    session = database.get_session(engine)
    database.seed_currencies(session)
    yield session


@pytest.fixture
def account(db_session: Session) -> Account:
    service = FinanceService(db_session)
    account = service.create_account(name="Test Account", currency_id="usd")
    return account


@pytest.fixture
def client(engine: Engine) -> TestClient:
    from src.main import app

    app.dependency_overrides[dependencies.engine] = lambda: engine

    return TestClient(app)


@pytest.fixture
def csv_file() -> BinaryIO:
    content = "date,description,amount\n"
    content += "2025-01-01,Test 1,100.00\n"
    content += "2025-01-01,Test 2,50.00\n"
    file = io.BytesIO(content.encode("utf-8"))
    return file
