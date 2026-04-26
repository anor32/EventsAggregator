from typing import Any

import httpx
from httpx import TimeoutException

from app.schemas.api import EventRegisterPost
from app.schemas.client import (
    EventsProviderResponseSchema as eventsResp,
    SeatsResponseSchema,
)
from app.settings.config import EVENTS_API_KEY
from app.settings.logs_config import api_logger
from app.utils import retry_request


class EventsProviderClient:
    _base_url = "http://events-provider.dev-2.python-labs.ru"
    _headers = {
        "x-api-key": EVENTS_API_KEY,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    async def fetch_page(self, url) -> dict[Any] | None:
        try:
            api_logger.info("Начало нового запроса")
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url=url,
                    headers=self._headers,
                    follow_redirects=True,
                )
                api_logger.info(
                    f"выполнен запрос к клиенту "
                    f"{response.status_code} url {response.request.url.path} "
                )

        except TimeoutException as e:
            api_logger.error(f"Превышено время ожидания от клиента {str(e)}")
            return None
        except httpx.ConnectError as e:
            api_logger.error(f"Ошибка подключения к {url}: {e}")
            return None
        except httpx.HTTPStatusError as e:
            api_logger.error(
                f"HTTP ошибка {e.response.status_code} при запросе к {url}"
            )
            return None
        except Exception as e:
            api_logger.error(
                f"Неизвестная ошибка при запросе к {url}: {type(e)}: {e}"
            )
            return None
        else:
            return response.json()

    async def get_pages(self, date) -> eventsResp:
        url = self._base_url + f"/api/events/?changed_at={date}/"
        response = await self.fetch_page(url)
        results = []
        if not response:
            api_logger.error("Запрос не был выполнен синхронизация неудалась")

        while response["next"]:
            url = response["next"]
            response = await self.fetch_page(url)
            results.extend(response["results"])

        return eventsResp(results=results)

    async def get_seats(self, event_id) -> SeatsResponseSchema:
        path = f"/api/events/{event_id}/seats/"
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self._base_url + path,
                headers=self._headers,
                follow_redirects=True,
                timeout=10,
            )

            if response.status_code > 404:
                response = await retry_request(
                    client, response.request, max_retry=3, delay=1
                )

        return SeatsResponseSchema(**response.json())

    async def register_to_event(self, event_id, body: EventRegisterPost):
        path = f"/api/events/{event_id}/register/"
        body = body.model_dump()
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self._base_url + path,
                headers=self._headers,
                follow_redirects=False,
                json=body,
                timeout=60,
            )
            if response.status_code == 308:
                new_url = response.headers["location"] + "/"
                new_response = await client.post(
                    new_url,
                    headers=self._headers,
                    follow_redirects=False,
                    json=body,
                    timeout=60,
                )

                return new_response.json()
        return response.json()

    async def unregister_to_event(self, event_id, body: dict[str, Any]):
        path = f"/api/events/{event_id}/unregister/"
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method="DELETE",
                url=self._base_url + path,
                json=body,
                headers=self._headers,
                follow_redirects=True,
                timeout=60,
            )
            return response.json()
