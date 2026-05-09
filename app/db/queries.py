from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert

from app.core.exceptions import ObjectNotFound
from app.db.models import Event, Place, Ticket
from app.schemas.api import ApiEventGetSchema
from app.schemas.base import TicketDbSchema
from app.schemas.client import ClientEventSchema
from app.settings.db_config import Base, Session
from app.settings.logs_config import api_logger


class DbRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_events_count(self, date_from) -> int:
        stmt = select(func.count()).select_from(Event)
        stmt = stmt.where(Event.event_time >= date_from)
        return self.session.scalar(stmt) or 0

    def get_all_events(
        self, page=1, page_size=20, date_from: datetime = None
    ) -> list[ApiEventGetSchema]:
        if not date_from:
            date_from = datetime.now()
        offset = (page - 1) * page_size
        stmt = (
            select(Event)
            .where(Event.event_time >= date_from)
            .where(Event.status == "published")
        )
        stmt = stmt.offset(offset).limit(page_size)
        events = self.session.scalars(stmt).all()
        results = [ApiEventGetSchema.model_validate(event) for event in events]

        return results

    def get_event(self, event_id) -> ApiEventGetSchema | str:
        event = self.session.scalars(
            select(Event).where(Event.id == event_id)
        ).first()

        if not event:
            raise ObjectNotFound("Событие не найдено в базе данных")
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

        return {"message": "success"}

    def get_event_last_date_updated(self):
        try:
            last_updated = self.session.scalars(
                select(Event.changed_at)
                .order_by(Event.changed_at.desc())
                .limit(1)
            ).all()
            if not last_updated:
                return datetime(2000, 1, 1)
        except Exception as e:
            api_logger.error("ошибка загрузки данных  в базу ", type(e), e)
        else:
            return last_updated[0]

    def get_event_by_ticket(self, ticket_id: str) -> str:
        print(ticket_id)
        ticket = self.session.scalars(
            select(Ticket).where(Ticket.id == ticket_id)
        ).first()

        if not ticket:
            raise ObjectNotFound("Подходящего cобтытия по билету не найдено")

        event_id = ticket.event
        return event_id

    def load_ticket(self, body: TicketDbSchema):
        ticket = Ticket(**body.model_dump())
        self.session.add(ticket)
        self.session.commit()

    def delete_ticket(self, ticket_id):
        ticket = self.session.scalars(
            select(Ticket).where(Ticket.id == ticket_id)
        ).first()
        if not ticket:
            raise ObjectNotFound("Подходящего билета не найдено")
        self.session.delete(ticket)
        self.session.commit()
