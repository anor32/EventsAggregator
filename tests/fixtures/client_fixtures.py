from unittest.mock import MagicMock, AsyncMock, patch

import pytest


from app.clients.event_client import EventsProviderClient
from app.schemas.api import EventRegisterPost
from app.schemas.base import EventDeleteRegister


@pytest.fixture
def client_instance():
    return EventsProviderClient()


@pytest.fixture
def register_body():
    return EventRegisterPost(
        event_id="event-123",
        first_name="Иван",
        last_name="Иванов",
        email="ivan@example.com",
        seat="A1"
    )


@pytest.fixture
def unregister_body():
    return EventDeleteRegister(ticket_id="ticket-123")


@pytest.fixture
def mock_httpx_client():
    with patch("httpx.AsyncClient") as MockClient:
        mock_client = MagicMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        MockClient.return_value = mock_client
        yield mock_client


@pytest.fixture
def test_event_data():
    return {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "name": "Test Event",
        "place": {
            "id": "123e4567-e89b-12d3-a456-426614174001",
            "name": "Test Place",
            "city": "Test City",
            "address": "Test Address",
            "seats_pattern": "A1-Z99"
        },
        "event_time": "2024-01-01T10:00:00",
        "registration_deadline": "2024-01-01T09:00:00",
        "status": "published",
        "number_of_visitors": 100,
        "changed_at": "2024-01-01T08:00:00",
        "created_at": "2024-01-01T08:00:00",
        "status_changed_at": "2024-01-01T08:00:00"
    }
