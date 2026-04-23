from uuid import UUID

from pydantic import BaseModel

from app.schemas.base import (
    EventSchema,
    RegisterEventSchema,
    UnregisterEventSchema,
)


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
