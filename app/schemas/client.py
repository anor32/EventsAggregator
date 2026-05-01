from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.schemas.base import EventSchema


class ClientEventSchema(EventSchema):
    id: UUID
    changed_at: datetime
    created_at: datetime
    status_changed_at: datetime


class SeatsResponseSchema(BaseModel):
    available_seats: list[str]
    event_id: str


class EventsResponseSchema(BaseModel):
    results: list[ClientEventSchema]

    model_config = ConfigDict(from_attributes=True)
