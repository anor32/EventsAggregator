import asyncio

from fastapi import HTTPException

from app.settings.logs_config import api_logger


async def retry_request(client, request, max_retry=3, delay=1):
    retry = 1
    response = await client.send(request)
    while retry <= max_retry:
        if response.status_code < 404:
            return response
        if response.status_code >= 404:
            print(response.status_code)
            retry += 1
            await asyncio.sleep(delay)
        response = await client.send(request)
    if response.status_code >= 500:
        raise ValueError("503|Ошибка внешнего сервера попробуйте позже")
    if response.status_code == 404:
        raise ValueError("404|Ошибка запрашиваемые данные не найдены")
    if response.status_code == 400:
        raise ValueError("400|Ошибка неправильный запрос клиента")

    return response


def default_endpoint_exception(func):
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
