from sqlalchemy import text
from sqlmodel import create_engine, Session, SQLModel

from src import base_categories
from src.models import Currency

engine = create_engine("sqlite:///finance-manager.db")
SQLModel.metadata.create_all(engine, checkfirst=True)


def get_session():
    with Session(engine) as session:
        session.exec(text("PRAGMA foreign_keys = ON;"))  # Enable foreign key constraints
        return session


def seed_db():
    seed_currencies()
    seed_categories()


def seed_categories():
    session = get_session()
    print("Seeding database with base categories")
    for category in base_categories.all_categories:
        session.add(category)
    session.commit()


def seed_currencies():
    print("Seeding database with currencies")

    session = get_session()
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
