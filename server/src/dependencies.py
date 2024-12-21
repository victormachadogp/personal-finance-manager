from fastapi import Depends
from src.services.finances import FinanceService
from src import database


def engine():
    return database.get_engine()


def get_session(engine=Depends(engine)):
    return database.get_session(engine)


def finance_service(session=Depends(get_session)):
    return FinanceService(session)
