from typing import Annotated

from fastapi import Depends

from app.clients.event_client import EventsProviderClient
from app.db.querries import DbQueries
from app.schemas.api import ApiGetPagesEvent
from app.services import EventService
from app.settings.db_config import Session


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


def get_service(db: Session = Depends(get_db)):
    client = EventsProviderClient()
    db = DbQueries(db)
    return EventService(db, client)


PagesSchema = Annotated[ApiGetPagesEvent, Depends()]
DbSession = Annotated[Session, Depends(get_db)]
EventServiceDep = Annotated[EventService, Depends(get_service)]
