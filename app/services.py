from uuid import UUID

from app.clients.event_client import EventsProviderClient
from app.db.querries import DbRepository
from app.schemas.api import (
    ApiEventGetSchema,
    ApiEventsSchema,
    ApiGetPagesEvent,
    EventRegisterPost,
)
from app.schemas.base import RegisterEventSchema
from app.schemas.client import SeatsResponseSchema


class EventService:
    def __init__(self, db: DbRepository, client: EventsProviderClient):
        self.client = client
        self.db = db

    async def sync_db(self, date="2000-01-01") -> dict[str, str]:
        resp = await self.client.get_events(date=date)
        last_changed_date = max(event.changed_at for event in resp.results)

        last_changed_date = last_changed_date.strftime("%Y-%m-%d")
        if date > last_changed_date:
            db_response = self.db.load_to_base(resp.results)
            db_response["last_changed_date"] = date
            print("here")
            return db_response
        else:
            print(
                f"cинхронизация по дате{date} не "
                f"требуется в базе данные от {last_changed_date},"
            )
            return {
                "message": "success",
                "last_changed_date": last_changed_date,
            }

    async def get_events(self, data: ApiGetPagesEvent) -> ApiEventsSchema:
        return self.db.get_all_events(
            data.page, data.page_size, data.date_from
        )

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
