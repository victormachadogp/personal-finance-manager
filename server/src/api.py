from typing import Optional
from fastapi import APIRouter, Depends, Query
from src.dtos import MonthYear
from src.services.finances import FinanceService
from src.dependencies import finance_service

router = APIRouter()

YearMonthQuery = Query(
    None,
    regex=r"^\d{4}-(0[1-9]|1[0-2])$",  # Regex to validate yyyy-mm format
    description="Month in yyyy-mm format",
)


def to_month_year(month: Optional[str]) -> Optional[MonthYear]:
    if month:
        year, month = month.split("-")
        return MonthYear(year=int(year), month=int(month))
    return None


@router.get("/transactions")
def get_transactions(
    finance_service: FinanceService = Depends(finance_service),
    month: Optional[str] = YearMonthQuery,
):
    month_filter = to_month_year(month)
    transactions = finance_service.get_transactions(month=month_filter)
    return transactions


@router.get("/categories")
def get_categories(finance_service: FinanceService = Depends(finance_service)):
    return finance_service.get_categories()


@router.get("/categories/analytics")
def get_analytics(
    finance_service: FinanceService = Depends(finance_service),
    month: Optional[str] = YearMonthQuery,
):
    month_filter = to_month_year(month)
    return finance_service.get_category_analytics(month=month_filter)
