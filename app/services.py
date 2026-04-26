from datetime import datetime
from uuid import UUID

from fastapi import Request

from app.clients.event_client import EventsProviderClient
from app.db.querries import DbRepository
from app.paginators import ApiPaginator
from app.schemas.api import (
    ApiEventGetSchema,
    ApiEventsSchema,
    ApiGetPagesEvent,
    EventRegisterPost,
)
from app.schemas.base import RegisterEventSchema
from app.schemas.client import SeatsResponseSchema
from app.settings.logs_config import api_logger


class EventService:
    def __init__(self, db: DbRepository, client: EventsProviderClient):
        self.client = client
        self.db = db

    async def sync_db(self, date: str | datetime = "2000-01-01") -> dict:
        api_logger.info("Получение данных от клиента")
        if isinstance(date, datetime):
            date = date.strftime("%Y-%m-%d")
        resp = await self.client.get_events(date=date)

        last_client_date = max(event.changed_at for event in resp.results)
        db_last_date = self.db.get_event_last_date_updated()
        last_client_date = last_client_date.replace(tzinfo=None)

        if last_client_date > db_last_date:
            db_response = self.db.load_to_base(resp.results)
            db_response["last_changed_date"] = last_client_date

            api_logger.info("Синхронизация успешно прошла")
            return db_response
        else:
            api_logger.info(
                f"cинхронизация по дате {date} не "
                f"требуется в базе данные от {last_client_date},"
            )

            return {
                "message": "success",
                "last_changed_date": last_client_date,
            }

    async def get_events(
        self, data: ApiGetPagesEvent, request: Request
    ) -> ApiEventsSchema:
        events = self.db.get_all_events(
            data.page, data.page_size, data.date_from
        )
        count = self.db.get_events_count(date_from=data.date_from)
        path = "/api/events"
        paginator = ApiPaginator(
            count, path, request, page=data.page - 1, page_size=data.page_size
        )
        next_url = paginator.get_next_url()
        previous_url = paginator.get_previous_url()
        schema = ApiEventsSchema(
            next=next_url, previous=previous_url, count=count, results=events
        )
        return schema

    async def event_detail(self, event_id: UUID | str) -> ApiEventGetSchema:
        return self.db.get_event(event_id)

    async def get_available_seats(self, event_id) -> SeatsResponseSchema:
        seats = await self.client.get_seats(event_id)
        return seats

    async def registration(self, event_id, body: EventRegisterPost):
        ticket = await self.client.register_to_event(event_id, body)
        return ticket

    async def un_registration(self, ticket_id, body: RegisterEventSchema):
        body = body.model_dump()
        message = await self.client.unregister_to_event(ticket_id, body)
        return message
