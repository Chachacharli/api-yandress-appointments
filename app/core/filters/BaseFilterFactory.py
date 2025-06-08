from typing import Generic, TypeVar

from sqlalchemy import and_, asc, desc
from sqlalchemy.orm import Query

from app.schemas.common import DateRange, Order, OrderBy

T = TypeVar("T")


class FilterFactory(Generic[T]):
    def __init__(self, model: type[T]):
        self.model = model
        self.filters = []
        self.sort = None

    def text(self, field_name: str, value: str | None):
        if value:
            self.filters.append(getattr(self.model, field_name).ilike(f"%{value}%"))

    def boolean(self, field_name: str, value: bool | None):
        if value is not None:
            self.filters.append(getattr(self.model, field_name) == value)

    def daterange(self, field_name: str, range_obj: DateRange | None):
        if range_obj:
            col = getattr(self.model, field_name)
            if range_obj.start_date:
                self.filters.append(col >= range_obj.start_date)
            if range_obj.end_date:
                self.filters.append(col <= range_obj.end_date)

    def order_by(self, order_by: OrderBy):
        if order_by is None or order_by.direction is None:
            return
        if order_by.direction.name == Order.none.name:
            return

        direction = order_by.direction
        field = order_by.field

        col = getattr(self.model, field, None)
        if col is None:
            return
        if direction == Order.asc.name:
            self.sort = asc(col)
        elif direction == Order.desc.name:
            self.sort = desc(col)

    def build(self, query: Query) -> Query:
        return query.filter(and_(*self.filters)) if self.filters else query
