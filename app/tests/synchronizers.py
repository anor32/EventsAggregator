import asyncio

from app.services import EventService


class BackgroundSynchronizer:

    def __init__(self, service: EventService):
        self._service = service

    async def synchronize(self, delay=24, date=None):
        print('Начат процесс синхронизации')
        if date is None:
            date = '2000-01-01'


        while True:
            print(f'Фоновавя синхронизация по дате {date}')
            sync_dict = await self._service.sync_db(date)
            date = sync_dict['last_changed_date']

            await asyncio.sleep(delay*60*60)
