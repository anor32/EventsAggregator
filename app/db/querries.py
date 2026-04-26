from datetime import datetime

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from app.db.models import Event, Place
from app.schemas.api import ApiEventGetSchema, ApiEventsSchema
from app.schemas.client import ClientEventSchema
from app.settings.db_config import Base, Session


class DbRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all_events(
        self, page=1, page_size=20, date_from: datetime = None
    ) -> ApiEventsSchema:
        if not date_from:
            date_from = datetime.now()
        offset = (page - 1) * page_size
        stmt = select(Event).where(Event.event_time >= date_from)
        stmt = stmt.offset(offset).limit(page_size)
        events = self.session.scalars(stmt).all()

        schema = ApiEventsSchema(next=None, previous=None, results=events)
        return schema

    def get_event(self, event_id) -> ApiEventGetSchema | str:
        event = self.session.scalars(
            select(Event).where(Event.id == event_id)
        ).one()
        if not event:
            raise ValueError("Ошибка 404 не найден в базе данных")
        return ApiEventGetSchema.model_validate(event)

    def _prepare_stmt_to_insert(self, Model: Base, data: list):
        update_fields = {}
        stmt = insert(Model).values(data)
        for column in stmt.excluded:
            if column.name != "id":
                update_fields[column.name] = column
        n_stmt = stmt.on_conflict_do_update(
            index_elements=["id"], set_=update_fields
        )
        return n_stmt

    def load_to_base(self, dates: list[ClientEventSchema]) -> dict[str, str]:
        event_data = []
        place_data = []
        for data in dates:
            en_data = data.model_dump(exclude={"place"})
            en_data["place_id"] = data.place.id
            place_dict = data.place.model_dump()

            if place_dict not in place_data:
                place_data.append(place_dict)
            event_data.append(en_data)
        p_stmt = self._prepare_stmt_to_insert(Place, place_data)
        e_stmt = self._prepare_stmt_to_insert(Event, event_data)

        self.session.execute(p_stmt)
        self.session.execute(e_stmt)
        self.session.commit()

        return {"msg": "success added"}

    def get_event_last_date_updated(self):
        last_updated = self.session.scalars(
            select(Event.changed_at).order_by(Event.changed_at.desc()).limit(1)
        ).all()
        if not last_updated:
            return datetime(2000, 1, 1)

        return last_updated[0]
