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
   return '007d362c-6c9d-4293-9f83-4f741de0056f'


@pytest_asyncio.fixture()
async def pages_body():
    return ApiGetPagesEvent(page=1,page_size=20,date_from='2001-01-01')


@pytest_asyncio.fixture()
async def register_user(event_id):
    data = {
         "id":  '007d362c-6c9d-4293-9f83-4f741de0056f',
         "first_name": "Иван",
         "last_name": "Иванов",
         "email": "ivan@example0.com",
         "seat": "B40"
    }
    return EventRegisterPost(**data)
