from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class Order(str, Enum):
    asc = "asc"
    desc = "desc"


class Pagination(BaseModel):
    page: int = 1
    size: int = 25


class DateRange(BaseModel):
    gte: datetime | None = None
    lte: datetime | None = None
