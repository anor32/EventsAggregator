from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.exceptions import ClientServerError, ObjectNotFound, WrongRequest
from app.settings.logs_config import api_logger


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except ObjectNotFound as e:
            api_logger.error(f"ошибка в эндпоинте{request.url} {e}")
            return JSONResponse(status_code=404, content={"detail": str(e)})
        except (ValueError, WrongRequest) as e:
            api_logger.error(f"ошибка в эндпоинте{request.url} {str(e)}")
            return JSONResponse(status_code=400, content={"detail": str(e)})
        except ClientServerError as e:
            api_logger.error(f"ошибка в эндпоинте{request.url} {str(e)}")
            return JSONResponse(
                status_code=e.status_code, content={"detail": str(e)}
            )
        except Exception as e:
            api_logger.error(f"Ошибка сервера: {e}", exc_info=True)
            return JSONResponse(
                status_code=500, content={"detail": "Внутренняя ошибка"}
            )
