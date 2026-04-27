from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.base import (
    EventSchema,
    RegisterEventSchema,
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
    count: int | None
    results: list[ApiEventGetSchema]

    model_config = ConfigDict(from_attributes=True)


class EventRegisterPost(RegisterEventSchema):
    id: str


class ApiSuccessSchema(BaseModel):
    success: bool


class ApiRegisterSchema(BaseModel):
    ticket_id: str


class EventDeleteRegister(RegisterEventSchema):
    ticket_id: str


class ApiGetPagesEvent(BaseModel):
    page: int | None = Field(1, ge=1)
    page_size: int | None = 20
    date_from: str | None = "2001-01-01"


class SynchronizeResponseSchema(BaseModel):
    message: str
