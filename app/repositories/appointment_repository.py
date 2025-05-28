from datetime import datetime
from uuid import UUID

from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from app.core.filters.BaseFilterFactory import FilterFactory
from app.models.appointment import Appointment
from app.schemas.appointment import (
    AppointmentCreate,
    AppointmentFilter,
    AppointmentUpdate,
)


class AppointmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_appointment(self, appointment: AppointmentCreate) -> Appointment:
        db_appointment = Appointment(**appointment.dict())
        self.db.add(db_appointment)
        self.db.commit()
        self.db.refresh(db_appointment)
        return db_appointment

    def get_appointments(self, filters: AppointmentFilter, params) -> list[Appointment]:
        query = self.db.query(Appointment)
        pagintion_filter = FilterFactory(Appointment)
        pagintion_filter = FilterFactory(Appointment)
        pagintion_filter.text("name", filters.name)
        pagintion_filter.text("phone", filters.phone)
        pagintion_filter.boolean("completed", filters.completed)
        pagintion_filter.daterange("create_at", filters.created)
        pagintion_filter.daterange("completed_at", filters.completed_date)

        query = pagintion_filter.build(query)

        return paginate(query, params=params)

    def get_appointment(self, appointment_id: UUID) -> Appointment | None:
        return (
            self.db.query(Appointment).filter(Appointment.id == appointment_id).first()
        )

    def update_appointment(self, update_data: AppointmentUpdate) -> Appointment | None:
        print("Updating appointment with ID:", update_data.id)
        appointment = (
            self.db.query(Appointment)
            .filter(Appointment.id == str(update_data.id))
            .first()
        )
        if not appointment:
            return None

        # Solo actualizamos los campos que no sean None
        if update_data.name is not None:
            appointment.name = update_data.name

        if update_data.phone is not None:
            appointment.phone = update_data.phone

        if update_data.notes is not None:
            appointment.notes = update_data.notes

        if update_data.completed is not None:
            appointment.completed = update_data.completed
            if update_data.completed:
                appointment.completed_at = update_data.completed_at or datetime.utcnow()
            else:
                appointment.completed_at = None

        if update_data.update_at is not None:
            appointment.update_at = update_data.update_at

        self.db.commit()
        self.db.refresh(appointment)
        return appointment

    def delete_appointment(self, appointment_id: UUID) -> bool:
        appointment = self.get_appointment(appointment_id)
        if not appointment:
            return False
        self.db.delete(appointment)
        self.db.commit()
        return True
