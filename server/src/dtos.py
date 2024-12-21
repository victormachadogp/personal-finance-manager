from typing import Optional
from pydantic import BaseModel
from sqlmodel import Field


class MonthYear(BaseModel):
    year: int
    month: int = Field(..., ge=1, le=12)

class ColumnMapper(BaseModel):
    date: str
    date_format: str  # eg: "%d/%m/%Y" or "%Y-%m-%d"
    description: str
    amount: str
    category: Optional[str] = None