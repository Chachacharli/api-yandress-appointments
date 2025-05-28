from uuid import UUID

from sqlalchemy.orm import Session

from app.models.appointment import Appointment
from app.repositories.appointment_repository import AppointmentRepository


class AppointmentService:
    def __init__(self, db: Session):
        self.db = db
        self.appointment_repository = AppointmentRepository(db)

    def create_appointment(self, appointment_data) -> Appointment:
        return self.appointment_repository.create_appointment(appointment_data)

    def get_appointments(self, filters, params) -> list[Appointment]:
        return self.appointment_repository.get_appointments(
            filters=filters, params=params
        )

    def get_appointment(self, appointment_id: UUID) -> Appointment | None:
        return self.appointment_repository.get_appointment(appointment_id)

    def update_appointment(
        self,
        appointment_data: Appointment,
    ) -> Appointment | None:
        return self.appointment_repository.update_appointment(appointment_data)

    def delete_appointment(self, appointment_id: UUID) -> bool:
        return self.appointment_repository.delete_appointment(appointment_id)
