import uuid
from datetime import datetime

from sqlalchemy import UUID, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.settings.db_config import Base


class Event(Base):
    __tablename__ = "Events"
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(), nullable=False)
    place_id: Mapped[UUID] = mapped_column(
        ForeignKey("places.id"), nullable=False
    )
    event_time: Mapped[datetime]
    registration_deadline: Mapped[datetime]
    status: Mapped[str]
    number_of_visitors: Mapped[int]
    changed_at: Mapped[datetime]
    created_at: Mapped[datetime]
    status_changed_at: Mapped[datetime]


class Place(Base):
    __tablename__ = "places"
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str]
    city: Mapped[str]
    address: Mapped[str]
    seats_pattern: Mapped[str]
