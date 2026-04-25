import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.schemas.api import ApiGetPagesEvent, EventRegisterPost



@pytest_asyncio.fixture()
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac



@pytest_asyncio.fixture()
async def event_id():
   return '3c141c94-bd42-4462-8d72-9a4f9d6007bc'


@pytest_asyncio.fixture()
async def pages_body():
    return ApiGetPagesEvent(page=1,page_size=20,date_from='2001-01-01')


@pytest_asyncio.fixture()
async def register_user(event_id):
    data = {
         "id":  str(event_id),
         "first_name": "Иван",
         "last_name": "Иванов",
         "email": "ivan@example.com",
         "seat": "B1"
    }
    return EventRegisterPost(**data)
