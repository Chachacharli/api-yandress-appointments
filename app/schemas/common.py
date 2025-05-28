from datetime import datetime
from enum import Enum
from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class Order(str, Enum):
    asc = "asc"
    desc = "desc"


class Pagination(BaseModel):
    page: int = 1
    size: int = 25


class DateRange(BaseModel):
    start_date: datetime | None = None
    end_date: datetime | None = None


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    size: int
