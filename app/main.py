import asyncio

from fastapi import FastAPI

from .clients.event_client import EventsProviderClient
from .db.querries import DbRepository
from .enpoints import router
from .services import EventService
from .settings.db_config import Session
from .tests.synchronizers import BackgroundSynchronizer


def lifespan(app: FastAPI):
    session = Session()
    db = DbRepository(session)
    client = EventsProviderClient()
    service = EventService(db, client)
    synchronizer = BackgroundSynchronizer(service)
    task = asyncio.create_task(synchronizer.synchronize())
    yield
    print("завершение работы приложения")

    task.cancel()


app = FastAPI(lifespan=lifespan)
app.include_router(router)
