from typing import Generic, TypeVar

from sqlalchemy import and_, asc, desc
from sqlalchemy.orm import Query

from app.models.appointment import Appointment
from app.schemas.common import DateRange, Order

T = TypeVar("T")


class FilterFactory(Generic[T]):
    def __init__(self, model: type[T]):
        self.model = model
        self.filters = []
        self.sort = None
        self.sort_column = None
        self.sort_direction = Order.none

    def text(self, field_name: str, value: str | None) -> Query:
        if value:
            self.filters.append(getattr(self.model, field_name).ilike(f"%{value}%"))

    def boolean(self, field_name: str, value: bool | None) -> Query:
        if value is not None:
            self.filters.append(getattr(self.model, field_name) == value)

    def daterange(self, field_name: str, range_obj: DateRange | None) -> Query:
        if range_obj:
            col = getattr(self.model, field_name)
            if range_obj.start_date:
                self.filters.append(col >= range_obj.start_date)
            if range_obj.end_date:
                self.filters.append(col <= range_obj.end_date)

    def order_by(self, order_by: str, direction: Order | None = None):
        if not order_by:
            self.sort_column = None
            self.sort_direction = Order.none
            return

        if not hasattr(self.model, order_by):
            raise ValueError(f"Invalid order_by field: {order_by}")

        self.sort_column = getattr(self.model, order_by)
        self.sort_direction = direction or Order.asc

    def build(self, query: Query) -> Query:
        if self.filters:
            query = query.filter(and_(*self.filters))

        if self.sort_column is not None:
            if self.sort_direction == Order.desc:
                query = query.order_by(desc(self.sort_column))
            else:
                query = query.order_by(asc(self.sort_column))
        return query
