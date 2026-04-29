import asyncio

from app.services import EventService
from app.settings.logs_config import api_logger


class BackgroundSynchronizer:
    def __init__(self, service: EventService):
        self._service = service

    async def synchronize(self, delay=24, date=None):
        api_logger.info("Начат процесс синхронизации")
        if date is None:
            date = "2000-01-01"

        while True:
            api_logger.info(f"Фоновавя синхронизация по дате {date}")
            sync_dict = await self._service.sync_db(date)
            if not sync_dict:
                api_logger.error(
                    "ошибка во время синхронизации повторный запрос "
                )
                continue
            date = sync_dict["last_changed_date"]
            api_logger.info("Фоновая синхронизация завершена ")
            await asyncio.sleep(delay * 60 * 60)
