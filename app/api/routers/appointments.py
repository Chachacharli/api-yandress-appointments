# app/api/appointments.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page, Params
from sqlalchemy.orm import Session

# from app.api.dependencies import (
#     get_current_user,  # Función que devuelve el usuario autenticado
# )
from app.database.session import get_db
from app.schemas.appointment import (
    AppointmentCreate,
    AppointmentDelete,
    AppointmentFilter,
    AppointmentRead,
    AppointmentUpdate,
)
from app.services.appointment_service import AppointmentService

router = APIRouter(prefix="/appointments", tags=["appointments"])


# Get all appointments
@router.get("/", response_model=Page[AppointmentRead])
async def get_all_appointments(
    filters: AppointmentFilter = Depends(),
    params: Params = Depends(),
    db: Session = Depends(get_db),
):
    """
    Get all appointments for the authenticated user.
    """
    try:
        appointments_service = AppointmentService(db)
        appointments = appointments_service.get_appointments(filters, params)
        return appointments
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        ) from e


# Get appointment by ID
@router.get("/{appointment_id}", response_model=AppointmentRead)
async def get_appointment(
    appointment_id: str,
    db: Session = Depends(get_db),
):
    """
    Get an appointment by ID.
    """
    try:
        appointment_service = AppointmentService(db)
        appointment = appointment_service.get_appointment(appointment_id)
        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Appointment not found",
            )
        return appointment
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        ) from e


# Create appointment
@router.post("/", response_model=AppointmentRead)
async def create_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new appointment.
    """
    try:
        appointment_service = AppointmentService(db)
        new_appointment = appointment_service.create_appointment(appointment)
        return new_appointment
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        ) from e


@router.delete("/{appointment_id}", response_model=AppointmentDelete)
async def delete_appointment(
    appointment_id: str,
    db: Session = Depends(get_db),
):
    """
    Delete an appointment by ID.
    """
    try:
        appointment_service = AppointmentService(db)
        deleted_appointment = appointment_service.delete_appointment(appointment_id)
        if not deleted_appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Appointment not found",
            )
        return {"detail": "Appointment deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        ) from e


@router.put("/{appointment_id}", response_model=AppointmentUpdate)
async def update_appointment(
    appointment: AppointmentUpdate,
    db: Session = Depends(get_db),
):
    """
    Update an appointment by ID.
    """
    try:
        appointment_service = AppointmentService(db)
        updated_appointment = appointment_service.update_appointment(appointment)
        if not updated_appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Appointment not found",
            )
        return updated_appointment
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        ) from e
