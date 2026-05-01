# tests/test_client.py
import pytest
from unittest.mock import AsyncMock, MagicMock, patch



@pytest.mark.asyncio
async def test_01_get_pages(client_instance, test_event_data):
    event = test_event_data.copy()
    event["id"] = "123e4567-e89b-12d3-a456-426614174000"
    event["name"] = "Test Event"

    mock_response = MagicMock()
    mock_response.is_success = True
    mock_response.json.return_value = {
        "results": [event],
        "next": None
    }

    mock_client = AsyncMock()
    mock_client.get = AsyncMock(return_value=mock_response)

    with patch("httpx.AsyncClient") as MockClient:
        MockClient.return_value.__aenter__.return_value = mock_client

        result = await client_instance.get_pages("2024-01-01")
        assert result is not None
        result = result.model_dump()
        assert len(result['results']) == 1
        assert str(result['results'][0]["id"]) == "123e4567-e89b-12d3-a456-426614174000"
        assert result['results'][0]["name"] == "Test Event"

@pytest.mark.asyncio
async def test_02_get_seats(client_instance):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"seats": ["A1", "A2"]}

    mock_client = MagicMock()
    mock_client.get = AsyncMock(return_value=mock_resp)
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)
    with patch("httpx.AsyncClient", return_value=mock_client):
        result = await client_instance.get_seats("event-123")
        assert result.available_seats == ["A1", "A2"]


@pytest.mark.asyncio
async def test_03_register_to_event(client_instance, register_body):
    mock_resp = MagicMock()
    mock_resp.is_success = True
    mock_resp.json.return_value = {"ticket_id": "ticket-123"}

    mock_client = MagicMock()
    mock_client.post = AsyncMock(return_value=mock_resp)
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)

    with patch("httpx.AsyncClient", return_value=mock_client):
        result = await client_instance.register_to_event("event-123", register_body)
        assert result["ticket_id"] == "ticket-123"


@pytest.mark.asyncio
async def test_04_unregister_to_event(client_instance, unregister_body):
    mock_resp = MagicMock()
    mock_resp.is_success = True

    mock_client = MagicMock()
    mock_client.request = AsyncMock(return_value=mock_resp)
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)

    with patch("httpx.AsyncClient", return_value=mock_client):
        result = await client_instance.unregister_to_event("event-123", unregister_body)
        assert result["success"] is True
