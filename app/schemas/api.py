from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.schemas.client import RegisterEventSchema, UnregisterEventSchema


class PlaceSchema(BaseModel):
    id: UUID
    name: str
    city: str
    address: str
    seats_pattern: str


class EventSchema(BaseModel):
    name: str
    place: PlaceSchema
    event_time: datetime
    registration_deadline: datetime
    status: str
    number_of_visitors: int


class GetEventSchema(EventSchema):
    id: UUID


class SeatsSchema(BaseModel):
    event_id: UUID
    available_seats: list[str]


class ApiEventGetSchema(BaseModel):
    next: str | None
    previous: str | None
    results: list[GetEventSchema]


class EventRegisterPost(RegisterEventSchema):
    id: UUID


class EventDeleteRegister(UnregisterEventSchema):
    id: UUID
