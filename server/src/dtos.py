from pydantic import BaseModel
from sqlmodel import Field


class MonthYear(BaseModel):
    year: int
    month: int = Field(..., ge=1, le=12)
