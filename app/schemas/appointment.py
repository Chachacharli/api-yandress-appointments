from datetime import datetime
from uuid import UUID

from fastapi import Query
from pydantic import BaseModel

from app.schemas.common import DateRange, Order


class AppointmentBase(BaseModel):
    name: str
    phone: str
    notes: str | None = None


class AppointmentCreate(AppointmentBase):
    create_at: datetime | None = None


class AppointmentUpdate(BaseModel):
    id: UUID
    name: str | None = None
    phone: str | None = None
    notes: str | None = None
    completed: bool = None
    update_at: datetime | None = None
    completed_at: datetime | None = None


class AppointmentRead(AppointmentBase):
    id: UUID
    name: str | None = None
    phone: str | None = None
    notes: str | None = None
    completed: bool = None
    update_at: datetime | None = None
    completed_at: datetime | None = None
    create_at: datetime | None = None

    class Config:
        from_attributes = True


class AppointmentDelete(BaseModel):
    id: UUID

    class Config:
        from_attributes = True


class AppointmentFilter:
    def __init__(
        self,
        name: str | None = None,
        phone: str | None = None,
        completed: bool | None = None,
        created_start: datetime | None = Query(None),
        created_end: datetime | None = Query(None),
        completed_start: datetime | None = Query(None),
        completed_end: datetime | None = Query(None),
        oder_by: str = "",
        direction: Order = Order.desc,
    ):
        self.name = name
        self.phone = phone
        self.completed = completed
        self.created = DateRange(start_date=created_start, end_date=created_end)
        self.completed_date = DateRange(
            start_date=completed_start, end_date=completed_end
        )
        self.oder_by = oder_by
        self.direction = direction
