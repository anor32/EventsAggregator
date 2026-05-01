from unittest.mock import MagicMock

import pytest
from app.core.paginators import ApiPaginator, ClientEventsPaginator


def test_api_paginator_01_get_next_url(api_paginator):
    next_url = api_paginator.get_next_url()
    assert next_url == "http://test.com/api/events?page=3&page_size=20"


def test_api_paginator_02_get_previous_url(api_paginator):
    prev_url = api_paginator.get_previous_url()
    assert prev_url == "http://test.com/api/events?page=1&page_size=20"


def test_api_paginator_03_get_next(api_paginator):
    api_paginator.page = 1
    api_paginator.max_pages = 5
    assert api_paginator.get_previous_url() is None

    for i in range(4):
        if i == 0:
            assert api_paginator.get_next_url() == "http://test.com/api/events?page=2&page_size=20"
        api_paginator.page += 1

    assert api_paginator.get_next_url() is None
    assert api_paginator.get_previous_url() == "http://test.com/api/events?page=4&page_size=20"


def test_api_paginator_04_get_previous_url_none_on_first_page():
    paginator = ApiPaginator(
        count_objects=100,
        path="/api/events",
        base_url="http://test.com",
        page=1,
        page_size=20
    )
    assert paginator.get_previous_url() is None


def test_api_paginator_05_edge_case_empty():
    paginator = ApiPaginator(
        count_objects=0,
        path="/api/events",
        base_url="http://test.com",
        page=1,
        page_size=20
    )
    assert paginator.max_pages == 0
    assert paginator.get_next_url() is None
    assert paginator.get_previous_url() is None


@pytest.mark.asyncio
async def test_client_paginator_06_iterates_over_pages(client_paginator_data):
    mock_client = client_paginator_data["client"]
    mock_client.get.side_effect = [
        MagicMock(json=lambda: {"results": [{"id": 1}], "next": "http://test.com/api/events?page=2"}),
        MagicMock(json=lambda: {"results": [{"id": 2}], "next": "http://test.com/api/events?page=3"}),
        MagicMock(json=lambda: {"results": [{"id": 3}], "next": None}),
    ]
    paginator = ClientEventsPaginator(**client_paginator_data)
    results = []
    async for response in paginator:
        results.extend(response.json().get("results", []))

    assert len(results) == 3
    assert results[0]["id"] == 1
    assert results[1]["id"] == 2
    assert results[2]["id"] == 3


@pytest.mark.asyncio
async def test_client_paginator_07_stops_when_no_next(client_paginator_data):
    mock_client = client_paginator_data["client"]

    response1 = MagicMock()
    response1.json.return_value = {"results": [{"id": 1}], "next": "http://test.com/api/events?page=2"}

    response2 = MagicMock()
    response2.json.return_value = {"results": [], "next": None}

    mock_client.get.side_effect = [response1, response2]

    paginator = ClientEventsPaginator(**client_paginator_data)

    count = 0
    async for _ in paginator:
        count += 1
    assert count == 2

@pytest.mark.asyncio
async def test_client_paginator_08_raises_stop_on_empty_url(client_paginator_data):
    data = client_paginator_data.copy()
    data["url"] = None
    paginator = ClientEventsPaginator(**data)

    with pytest.raises(StopAsyncIteration):
        await paginator.__anext__()


@pytest.mark.asyncio
async def test_client_paginator_09_updates_url(client_paginator_data):
    mock_client = client_paginator_data["client"]


    response = MagicMock()
    response.json.return_value = {
        "results": [{"id": 1}],
        "next": "http://test.com/api/events?page=2"
    }
    mock_client.get.return_value = response

    paginator = ClientEventsPaginator(**client_paginator_data)
    await paginator.__anext__()

    assert paginator.url == "http://test.com/api/events?page=2"
