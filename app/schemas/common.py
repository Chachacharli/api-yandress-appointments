from datetime import datetime
from enum import Enum
from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class Order(str, Enum):
    asc = "asc"
    desc = "desc"
    none = "none"


class OrderBy(BaseModel):
    field: str = Field(default=None, alias="field", description="Campo para ordenar")
    direction: Order = Field(
        default=Order.none, alias="order", description="Dirección de la orden"
    )

    class Config:
        use_enum_values = True
        from_attributes = True


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
