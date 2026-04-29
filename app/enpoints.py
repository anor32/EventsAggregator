from fastapi import APIRouter, Request

from app.schemas.api import (
    ApiEventGetSchema,
    ApiEventsSchema,
    ApiRegisterSchema,
    ApiUnregisterSchema,
    EventRegisterPost,
    SynchronizeResponseSchema,
)
from app.schemas.client import SeatsResponseSchema
from app.schemas.dependecies import EventServiceDep, PagesSchema
from app.settings.logs_config import api_logger

router = APIRouter()


@router.get("/api/health", status_code=200)
async def health():
    return {"status": "ok"}


@router.post("/api/sync/trigger")
async def manual_sync(
    service: EventServiceDep,
) -> SynchronizeResponseSchema:
    api_logger.info("Запуск ручной синхронизации ")
    resp = await service.sync_db()
    schema = SynchronizeResponseSchema(message=resp["message"])

    return schema


@router.get("/api/events")
async def get_events(
    data: PagesSchema,
    service: EventServiceDep,
    request: Request,
) -> ApiEventsSchema:
    resp = await service.get_events(data, request=request)

    return resp


@router.get("/api/events/{event_id}")
async def event_detail(
    event_id: str, service: EventServiceDep
) -> ApiEventGetSchema | dict:
    resp = await service.event_detail(event_id)

    return resp


@router.get("/api/events/{event_id}/seats")
async def event_seats(
    event_id: str, service: EventServiceDep
) -> SeatsResponseSchema:
    resp = await service.get_available_seats(event_id)

    return resp


@router.post("/api/tickets", status_code=201)
async def event_register(
    body: EventRegisterPost, service: EventServiceDep
) -> ApiRegisterSchema:
    resp = await service.registration(event_id=body.event_id, body=body)

    return resp


@router.delete("/api/tickets/{ticket_id}")
async def cancel_register(
    service: EventServiceDep, ticket_id: str
) -> ApiUnregisterSchema:
    resp = await service.un_registration(ticket_id)

    return resp
