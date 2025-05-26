from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import func

from app.database.base import Base


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid4()))
    user_google_id = Column(String(255), index=True)
    name = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=False)
    create_at = Column(DateTime, nullable=False, server_default=func.now())
    update_at = Column(
        DateTime, nullable=False, onupdate=func.now(), server_default=func.now()
    )
    notes = Column(String(500), nullable=True)
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True, server_default=None)
