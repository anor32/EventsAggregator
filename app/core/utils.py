import asyncio
from urllib.parse import urljoin

from httpx import AsyncClient, Request, Response

from app.core.exceptions import ClientServerError, ObjectNotFound, WrongRequest


async def retry_request(
    client: AsyncClient, request: Request, max_retry=3, delay=1
) -> Response:
    retry = 1
    response = await client.send(request)
    while retry <= max_retry and response.status_code >= 500:
        retry += 1
        await asyncio.sleep(delay)
        response = await client.send(request)

    if response.is_success:
        return response
    elif response.status_code >= 500:
        raise ClientServerError(
            "Ошибка внешнего сервера попробуйте позже", status_code=503
        )
    elif response.status_code == 404:
        raise ObjectNotFound(
            "Ошибка запрашиваемые данные от клиента не найдены "
        )
    elif response.status_code == 400:
        raise WrongRequest(
            f"Ошибка неправильный запрос клиента {response.text}", 400
        )


def build_url(base_url: str, path: str) -> str:
    base = base_url.rstrip("/")
    path = path.lstrip("/")
    return urljoin(base + "/", path)
