from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.common import DateRange, OrderBy


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

    class Config:
        from_attributes = True


class AppointmentDelete(BaseModel):
    id: UUID

    class Config:
        from_attributes = True


class AppointmentFilter(BaseModel):
    name: str | None = None
    phone: str | None = None
    completed: bool | None = None
    created: DateRange | None = None
    completed_date: DateRange | None = None
