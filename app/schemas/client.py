from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.schemas.base import EventSchema


class ClientEventSchema(EventSchema):
    id: UUID
    changed_at: datetime
    created_at: datetime
    status_changed_at: datetime


class SeatsResponseSchema(BaseModel):
    seats: str


class EventsProviderResponseSchema(BaseModel):
    next: str | None
    previous: str | None
    results: list[ClientEventSchema]
