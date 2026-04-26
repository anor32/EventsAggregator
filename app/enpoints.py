from fastapi import APIRouter, HTTPException, Request

from app.schemas.api import (
    ApiEventGetSchema,
    ApiEventsSchema,
    EventRegisterPost,
    SynchronizeResponseSchema,
)
from app.schemas.dependecies import EventServiceDep, PagesSchema
from app.settings.logs_config import api_logger
from app.utils import default_endpoint_exception

router = APIRouter()


@router.get("/api/health", status_code=200)
async def health():
    return {"status": "ok"}


@router.post("/api/sync/trigger")
async def manual_sync(service: EventServiceDep) -> SynchronizeResponseSchema:
    api_logger.info("Запуск ручной синхронизации ")
    try:
        resp = await service.sync_db()
        schema = SynchronizeResponseSchema(message=resp["message"])
    except ValueError as e:
        print(e)
    except Exception as e:
        api_logger.error(f"ошибка в эндпоните /api/sync/trigger {e}")
        message = "Внутреняя ошибка сервера "
        raise HTTPException(status_code=500, detail=message)
    else:
        api_logger.info("Ручная синхронизация завершена")
        return schema


@router.get("/api/events")
async def get_events(
    data: PagesSchema,
    service: EventServiceDep,
    request: Request,
) -> ApiEventsSchema | dict[str, str]:
    try:
        resp = await service.get_events(data, request=request)
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        api_logger.error(f"ошибка в эндпоните /api/events {e}")
        message = f"Внутреняя ошибка сервера{e}"
        raise HTTPException(status_code=500, detail=message)
    else:
        return resp


@default_endpoint_exception
@router.get("/api/events/{event_id}")
async def event_detail(
    event_id, service: EventServiceDep
) -> ApiEventGetSchema | dict:
    resp = await service.event_detail(event_id)

    return resp


@default_endpoint_exception
@router.get("/api/events/{event_id}/seats")
async def event_seats(event_id, service: EventServiceDep):
    resp = await service.get_available_seats(event_id)

    return resp


@default_endpoint_exception
@router.post("/api/tickets", status_code=201)
async def event_register(body: EventRegisterPost, service: EventServiceDep):
    resp = await service.registration(event_id=body.id, body=body)
    return resp


@default_endpoint_exception
@router.delete("/api/tickets/{ticket_id}")
async def cancel_register(ticket_id, body, service: EventServiceDep):
    resp = service.un_registration(ticket_id=ticket_id, json=body)

    return resp
