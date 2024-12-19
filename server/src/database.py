from sqlmodel import create_engine, Session, SQLModel

from src import base_categories

engine = create_engine("sqlite:///finance-manager.db")
SQLModel.metadata.create_all(engine, checkfirst=True)


def get_session():
    with Session(engine) as session:
        return session


def seed_db():
    print("Seeding database with base categories")
    with Session(engine) as session:
        for category in base_categories.all_categories:
            session.add(category)
        session.commit()
