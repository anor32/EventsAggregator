from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class EventStatus(str, Enum):
    PUBLISHED = "published"
    REGISTRATION_CLOSED = "registration_closed"
    FINISHED = "finished"


class PlaceSchema(BaseModel):
    id: UUID
    name: str
    city: str
    address: str
    seats_pattern: str

    model_config = ConfigDict(from_attributes=True)


class EventSchema(BaseModel):
    name: str
    place: PlaceSchema
    event_time: datetime
    registration_deadline: datetime
    status: EventStatus
    number_of_visitors: int


class EventDeleteRegister(BaseModel):
    ticket_id: str


class RegisterEventSchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    seat: str


class TicketDbSchema(BaseModel):
    id: str
    event: str
    seat: str

    model_config = ConfigDict(from_attributes=True)
