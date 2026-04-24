from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


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
    status: str
    number_of_visitors: int


class RegisterEventSchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    seat: str


class UnregisterEventSchema(BaseModel):
    ticket: UUID
