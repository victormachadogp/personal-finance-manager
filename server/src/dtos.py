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

    # convert date, description, amount, category to lowercase
    def __init__(self, **data):
        super().__init__(**{k: v.lower() if isinstance(v, str) and k != "date_format" else v for k, v in data.items()})
