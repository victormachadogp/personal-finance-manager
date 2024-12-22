from sqlalchemy import text
from sqlmodel import create_engine, Session, SQLModel

from src import base_categories
from src.models import Currency


def get_engine():
    engine = create_engine("sqlite:///finance-manager.db")
    SQLModel.metadata.create_all(engine, checkfirst=True)
    return engine


def get_session(engine):
    with Session(engine) as session:
        session.exec(text("PRAGMA foreign_keys = ON;"))  # Enable foreign key constraints
        return session


def seed_db():
    engine = get_engine()
    session = get_session(engine)
    seed_currencies(session=session)
    seed_categories(session=session)


def seed_categories(session: Session):
    print("Seeding database with base categories")
    for category in base_categories.all_categories:
        session.add(category)
    session.commit()


def seed_currencies(session: Session):
    print("Seeding database with currencies")

    # Seed currencies
    usd = Currency(id="usd", name="United States Dollar", code="USD", symbol="$")
    gbp = Currency(id="gbp", name="British Pound", code="GBP", symbol="£")
    eur = Currency(id="eur", name="Euro", code="EUR", symbol="€")
    brl = Currency(id="brl", name="Brazilian Real", code="BRL", symbol="R$")
    session.add(usd)
    session.add(gbp)
    session.add(eur)
    session.add(brl)

    session.commit()
