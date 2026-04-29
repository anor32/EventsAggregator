import asyncio

from fastapi import FastAPI

from .api.endpoints import router
from .api.middlewares import ErrorHandlingMiddleware
from .clients.event_client import EventsProviderClient
from .core.synchronizers import BackgroundSynchronizer
from .db.querries import DbRepository
from .services import EventService
from .settings.db_config import Session


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
app.add_middleware(ErrorHandlingMiddleware)

app.include_router(router)
