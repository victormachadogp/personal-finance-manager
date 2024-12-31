from typing import Optional, Sequence
from fastapi import APIRouter, Depends, File, Form, Query, UploadFile
from pydantic import BaseModel
from src.dtos import ColumnMapper, MonthYear, UpdateTransaction
from src.models import Category, Transaction
from src.services.finances import CategoryAnalyticsRespose, FinanceService
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
    category_id: Optional[str] = Query(None, description="Filter by category"),
) -> Sequence[Transaction]:
    month_filter = to_month_year(month)
    transactions = finance_service.get_transactions(month=month_filter, category_id=category_id)
    return transactions


@router.patch("/transactions/{transaction_id}")
def update_transaction(
    transaction_id: str,
    update_transaction: UpdateTransaction,
    finance_service: FinanceService = Depends(finance_service),
) -> Transaction:
    transaction = finance_service.update_transaction(transaction_id, update_transaction)
    return transaction


@router.get("/categories")
def get_categories(finance_service: FinanceService = Depends(finance_service)) -> Sequence[Category]:
    return finance_service.get_categories()


@router.get("/categories/analytics")
def get_analytics(
    finance_service: FinanceService = Depends(finance_service),
    month: Optional[str] = YearMonthQuery,
) -> CategoryAnalyticsRespose:
    month_filter = to_month_year(month)
    return finance_service.get_category_analytics(month=month_filter)


# Schemas can be moved to a separate file
class CurrencySchema(BaseModel):
    id: str
    name: str
    code: str
    symbol: str
    model_config = {"from_attributes": True}


class AccountSchema(BaseModel):
    id: str
    name: str
    currency: CurrencySchema
    model_config = {"from_attributes": True}


@router.get("/accounts")
def get_accounts(finance_service: FinanceService = Depends(finance_service)) -> Sequence[AccountSchema]:
    accounts = finance_service.get_accounts()
    return [AccountSchema.model_validate(account) for account in accounts]


@router.post("/accounts/{account_id}/transactions/import")
def upload_transactions_csv(
    account_id: str,
    column_mapper: str = Form(...),
    file: UploadFile = File(...),
    finance_service: FinanceService = Depends(finance_service),
):
    _column_mapper = ColumnMapper.parse_raw(column_mapper)
    finance_service.import_csv(file=file.file, account_id=account_id, column_mapper=_column_mapper)
    return ""
