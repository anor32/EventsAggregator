from fastapi import APIRouter, HTTPException, Request

from app.schemas.api import (
    ApiEventGetSchema,
    ApiEventsSchema,
    ApiRegisterSchema,
    ApiSuccessSchema,
    EventRegisterPost,
    SynchronizeResponseSchema,
)
from app.schemas.dependecies import EventServiceDep, PagesSchema
from app.settings.logs_config import api_logger

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
        api_logger.error(f"ошибка в эндпоните /api/events {str(e)}")
        message = "Внутреняя ошибка сервера"
        raise HTTPException(status_code=500, detail=message)
    else:
        return resp


@router.get("/api/events/{event_id}")
async def event_detail(
    event_id: str, service: EventServiceDep
) -> ApiEventGetSchema | dict:
    try:
        resp = await service.event_detail(event_id)
    except ValueError as e:
        status, message = str(e).split("|")
        print("here")
        raise HTTPException(status_code=int(status), detail=message)
    except Exception as e:
        api_logger.error(e)
        message = "Внутреняя ошибка сервера"
        raise HTTPException(status_code=500, detail=message)
    else:
        return resp


@router.get("/api/events/{event_id}/seats")
async def event_seats(event_id: str, service: EventServiceDep):
    try:
        resp = await service.get_available_seats(event_id)
    except ValueError as e:
        status, message = str(e).split("|")
        print("here")
        raise HTTPException(status_code=int(status), detail=message)
    except Exception as e:
        api_logger.error(e)
        message = "Внутреняя ошибка сервера"
        raise HTTPException(status_code=500, detail=message)
    else:
        return resp


@router.post("/api/tickets", status_code=201)
async def event_register(
    body: EventRegisterPost, service: EventServiceDep
) -> ApiRegisterSchema:
    try:
        resp = await service.registration(event_id=body.id, body=body)
    except ValueError as e:
        api_logger.error(e)
        status, message = str(e).split("|")
        raise HTTPException(status_code=int(status), detail=message)
    except Exception as e:
        api_logger.error(e)
        message = "Внутреняя ошибка сервера"
        raise HTTPException(status_code=500, detail=message)
    else:
        return resp


@router.delete("/api/tickets/{ticket_id}")
async def cancel_register(
    service: EventServiceDep, ticket_id: str
) -> ApiSuccessSchema:
    try:
        resp = await service.un_registration(ticket_id)
    except ValueError as e:
        status, message = str(e).split("|")
        raise HTTPException(status_code=int(status), detail=message)
    except Exception as e:
        api_logger.error(e)
        raise HTTPException(status_code=500, detail="Внутреняя ошибка сервера")
    else:
        return resp
