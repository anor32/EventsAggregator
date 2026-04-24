from datetime import datetime
from uuid import UUID

from app.clients.event_client import EventsProviderClient
from app.db.querries import DbQueries
from app.schemas.api import ApiEventGetSchema, ApiEventsSchema
from app.settings.db_config import Session


class EventService:
    def __init__(self, db: DbQueries, client: EventsProviderClient):
        self.client = client
        self.db = db

    async def sync_db(self) -> dict[str]:
        today = datetime.now().strftime("%Y-%m-%d")
        resp = await self.client.get_events(date=today)
        print(resp)
        # message = self.db.load_to_base(resp.results)
        return resp

    async def get_events(self, date_from: datetime = None) -> ApiEventsSchema:
        if not date_from:
            date_from = datetime.now().strftime("%Y-%m-%d")
        return self.db.get_all_events(date_from)

    async def event_detail(self, event_id: UUID | str) -> ApiEventGetSchema:
        return self.db.get_event(event_id)


client = EventsProviderClient()
session = Session()
db = DbQueries(session=session)
e = EventService(db=db, client=client)


event_id = "3c141c94-bd42-4462-8d72-9a4f9d6007bc"
# pprint(asyncio.run(e.sync_db()))
