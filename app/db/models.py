import uuid
from datetime import datetime

from sqlalchemy import UUID, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

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

    place: Mapped["Place"] = relationship(back_populates="events")


class Place(Base):
    __tablename__ = "places"
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str]
    city: Mapped[str]
    address: Mapped[str]
    seats_pattern: Mapped[str]

    events: Mapped[list["Event"]] = relationship(back_populates="place")


# class User(Base):
#     __tablename__ = 'users'
#     id: Mapped[UUID] = mapped_column(
#         UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
#     )
#     first_name:Mapped[str]
#     last_name:Mapped[str]
#     email:Mapped[str]
#


class Ticket(Base):
    __tablename__ = "tickets"
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    event: Mapped[uuid] = mapped_column(
        ForeignKey("Events.id"), nullable=False
    )
    seat: Mapped[str]

    # user: Mapped[int] = mapped_column(ForeignKey('users.id'),nullable=False)
