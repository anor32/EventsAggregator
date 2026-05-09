import asyncio
import logging

from fastapi import FastAPI

from app.api.endpoints import router
from app.api.middlewares import ErrorHandlingMiddleware
from app.clients.event_client import EventsProviderClient
from app.core.synchronizers import BackgroundSynchronizer
from app.db.queries import DbRepository
from app.services import EventService
from app.settings.db_config import Session

logger = logging.getLogger(__name__)


def lifespan(app: FastAPI):
    session = Session()  # <-- исправлено Session()
    db = DbRepository(session)
    client = EventsProviderClient()
    service = EventService(db, client)
    synchronizer = BackgroundSynchronizer(service)

    task = asyncio.create_task(synchronizer.synchronize())

    yield

    logger.info("Завершение работы приложения")

    task.cancel()
    try:
        asyncio.get_running_loop().run_until_complete(task)
    except asyncio.CancelledError:
        pass
    finally:
        session.close()


app = FastAPI(lifespan=lifespan)
app.add_middleware(ErrorHandlingMiddleware)
app.include_router(router)
