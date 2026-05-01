from unittest.mock import AsyncMock, MagicMock

import pytest

from app.core.paginators import ApiPaginator


@pytest.fixture
def api_paginator():
    return ApiPaginator(
        count_objects=100,
        path="/api/events",
        base_url="http://test.com",
        page=2,
        page_size=20
    )

@pytest.fixture
def mock_async_client():
    mock = AsyncMock()

    mock_response = MagicMock()
    mock_response.json.return_value = {"results": [], "next": None}


    mock.get = AsyncMock(return_value=mock_response)

    return mock

@pytest.fixture
def client_paginator_data(mock_async_client):
    return {
        "url": "http://test.com/api/events?page=1",
        "client": mock_async_client,
        "headers": {"X-API-Key": "test-key"}
    }
