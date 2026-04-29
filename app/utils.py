import asyncio
from collections.abc import Callable

from fastapi import HTTPException
from httpx import AsyncClient, Request, Response

from app.exceptions import ClientServerError, ObjectNotFound, WrongRequest
from app.settings.logs_config import api_logger


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


def default_endpoint_exception(func: Callable):
    async def wrapper():
        try:
            resp = await func()
        except ValueError as e:
            status, message = str(e).split("|")
            print("here")
            raise HTTPException(status_code=int(status), detail=message)
        except Exception as e:
            api_logger.error(e)
            message = f"Внутреняя ошибка сервера{e}"
            raise HTTPException(status_code=500, detail=message)
        else:
            return resp

    return wrapper
