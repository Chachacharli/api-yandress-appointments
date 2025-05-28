from typing import Generic, TypeVar

from sqlalchemy import and_
from sqlalchemy.orm import Query

from app.schemas.common import DateRange

T = TypeVar("T")


class FilterFactory(Generic[T]):
    def __init__(self, model: type[T]):
        self.model = model
        self.filters = []

    def text(self, field_name: str, value: str | None):
        if value:
            self.filters.append(getattr(self.model, field_name).ilike(f"%{value}%"))

    def boolean(self, field_name: str, value: bool | None):
        if value is not None:
            self.filters.append(getattr(self.model, field_name) == value)

    def daterange(self, field_name: str, range_obj: DateRange | None):
        if range_obj:
            col = getattr(self.model, field_name)
            if range_obj.gte:
                self.filters.append(col >= range_obj.gte)
            if range_obj.lte:
                self.filters.append(col <= range_obj.lte)

    def sort(self, field_name: str, order: str = "asc"):
        if order == "asc":
            self.filters.append(getattr(self.model, field_name).asc())
        elif order == "desc":
            self.filters.append(getattr(self.model, field_name).desc())

    def build(self, query: Query) -> Query:
        return query.filter(and_(*self.filters)) if self.filters else query
