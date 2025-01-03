from sqlmodel import create_engine, Session, SQLModel

from src import base_categories
from src.models import Currency


def get_engine():
    engine = create_engine("sqlite:///finance-manager.db")
    SQLModel.metadata.create_all(engine, checkfirst=True)
    with engine.connect() as connection:
        # Enable foreign key constraints. Ensure it’s set once for all sessions
        connection.exec_driver_sql("PRAGMA foreign_keys = ON;")
    return engine


def get_session(engine):
    # https://sqlmodel.tiangolo.com/tutorial/fastapi/session-with-dependency/#create-a-fastapi-dependency
    with Session(engine) as session:
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
    usd = Currency(id="usd", name="United States Dollar", symbol="$", bcp_47_lang_tag="en-US")
    gbp = Currency(id="gbp", name="British Pound", symbol="£", bcp_47_lang_tag="en-GB")
    eur = Currency(id="eur", name="Euro", symbol="€", bcp_47_lang_tag="und-EU")
    brl = Currency(id="brl", name="Brazilian Real", symbol="R$", bcp_47_lang_tag="pt-BR")
    session.add(usd)
    session.add(gbp)
    session.add(eur)
    session.add(brl)

    session.commit()
