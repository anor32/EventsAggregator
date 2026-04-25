from fastapi import APIRouter, HTTPException

from app.schemas.api import (
    ApiEventGetSchema,
    ApiEventsSchema,
    EventRegisterPost,
)
from app.schemas.dependecies import EventServiceDep, PagesSchema

router = APIRouter()


@router.get("/api/health", status_code=200)
async def health():
    return {"status": "ok"}


@router.post("/api/sync/trigger")
async def manual_sync(service: EventServiceDep) -> dict[str, str]:
    resp = await service.sync_db()
    return {"msg": resp}


@router.get("/api/events")
async def get_events(
    data: PagesSchema, service: EventServiceDep
) -> ApiEventsSchema:
    try:
        resp = await service.get_events(data)
    except ValueError as e:
        return {"error": str(e)}
    return resp


@router.get("/api/events/{event_id}")
async def event_detail(
    event_id, service: EventServiceDep
) -> ApiEventGetSchema | dict:
    try:
        resp = await service.event_detail(event_id)
    except ValueError as e:
        return {"error": str(e)}
    return resp


@router.get("/api/events/{event_id}/seats")
async def event_seats(event_id, service: EventServiceDep):
    try:
        resp = await service.get_available_seats(event_id)
    except ValueError as e:
        status, message = str(e).split("|")
        raise HTTPException(status_code=int(status), detail=message)
    except Exception:
        message = "Внутреняя ошибка сервера"
        raise HTTPException(status_code=500, detail=message)
    return resp


@router.post("/api/tickets", status_code=201)
async def event_register(body: EventRegisterPost, service: EventServiceDep):
    try:
        resp = await service.registration(event_id=body.id, body=body)

    except ValueError as e:
        status, message = str(e).split("|")
        raise HTTPException(status_code=int(status), detail=message)
    except Exception as e:
        message = f"Внутреняя ошибка сервера {e}"
        raise HTTPException(status_code=500, detail=message)
    return resp


@router.delete("/api/tickets/{ticket_id}")
async def cancel_register(ticket_id, body, service: EventServiceDep):
    resp = service.un_registration(ticket_id=ticket_id, json=body)

    return resp
