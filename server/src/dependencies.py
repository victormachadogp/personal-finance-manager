from fastapi import Depends
from src.services.finances import FinanceService
from src import database


def get_session():
    return database.get_session()


def finance_service(session=Depends(get_session)):
    return FinanceService(session)
