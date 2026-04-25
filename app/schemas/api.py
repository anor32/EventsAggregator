from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.base import (
    EventSchema,
    RegisterEventSchema,
    UnregisterEventSchema,
)


class ApiEventGetSchema(EventSchema):
    id: UUID

    model_config = ConfigDict(from_attributes=True)


class SeatsSchema(BaseModel):
    event_id: UUID
    available_seats: list[str]


class ApiEventsSchema(BaseModel):
    next: str | None
    previous: str | None
    results: list[ApiEventGetSchema]

    model_config = ConfigDict(from_attributes=True)


class EventRegisterPost(RegisterEventSchema):
    id: str


class EventDeleteRegister(UnregisterEventSchema):
    id: UUID


class ApiGetPagesEvent(BaseModel):
    page: int = Field(1, ge=1)
    page_size: int = 20
    date_from: datetime = Field(default_factory=datetime.now)
