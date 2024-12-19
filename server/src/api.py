from fastapi import APIRouter, Depends
from src.services.finances import FinanceService
from src.dependencies import finance_service

router = APIRouter()


@router.get("/transactions")
def get_transactions(finance_service: FinanceService = Depends(finance_service)):
    transactions = finance_service.get_transactions()
    return transactions

@router.get("/categories")
def get_categories(finance_service: FinanceService = Depends(finance_service)):
    return finance_service.get_categories()

@router.get("/categories/analytics")
def get_analytics(finance_service: FinanceService = Depends(finance_service)):
    return finance_service.get_category_analytics()