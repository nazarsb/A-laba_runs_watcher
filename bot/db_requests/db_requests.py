import logging

from sqlalchemy import Date, case, cast, func, insert, literal, select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.dialects.postgresql import insert as upsert

from database.models import Event, Instrument, Reagent, EventType, User
from database.enums.enums import UserRole


logger = logging.getLogger(__name__)


async def get_instrument_names(session: AsyncSession) -> list:
    stmt = select(
        Instrument.name,
        Instrument.name
    )

    result = await session.execute(stmt)
    return result.all()


async def get_reagents(instrument: str, session: AsyncSession) -> list:
    stmt = select(
        Reagent.name,
        Reagent.name
    ).where(Reagent.instrument_id == (select(Instrument.id).where(Instrument.name == instrument)))

    result = await session.execute(stmt)
    return result.all()


async def get_runtime(selected_reagents: str, session: AsyncSession) -> list:
    stmt = select(
        Reagent.run_duration
    ).where(Reagent.name == selected_reagents)

    result = await session.execute(stmt)
    return result.first()[0]
    

async def insert_event(event_type_name: str,
                       event_name: str | None,
                       instrument_name: str | None,
                       reagent_name: str | None,
                       event_start_date: str,
                       event_end_date: str,
                       time_start: str | None,
                       time_end: str | None,
                       is_there_time: bool, 
                       session: AsyncSession) -> None:

    stmt = insert(Event).values(
        event_type_id=(select(EventType.id).where(EventType.name == event_type_name)),
        event_name=event_name if event_name else None,
        instrument_id=(select(Instrument.id).where(Instrument.name == instrument_name)),
        reagent_id=(select(Reagent.id).where(Reagent.name == reagent_name)),
        event_start_date=event_start_date,
        event_end_date=event_end_date,
        time_start=time_start if time_start else '12:00',
        time_end=time_end if time_end else '19:00',
        is_there_time=is_there_time
    )
    await session.execute(stmt)
    await session.commit()


async def get_events(session: AsyncSession) -> list:
    stmt = select(Event).options(joinedload(Event.instrument), 
                                 joinedload(Event.reagent), 
                                 joinedload(Event.event_type)) \
    .filter(cast(Event.event_end_date, Date) >= func.current_date()) \
    .order_by(Event.event_start_date, Event.event_end_date)
    result = await session.execute(stmt)
    events = result.scalars().all()
    
    return [{
        'id': event.id,
        'event_type': event.event_type.name,
        'event_name': event.event_name,
        'instrument': event.instrument.name if event.instrument else None,
        'reagent': event.reagent.name if event.reagent else None,
        'date_start': event.event_start_date,
        'date_end': event.event_end_date,
        'time_start': event.time_start if event.is_there_time else None,
        'time_end': event.time_end if event.is_there_time else None
    } for event in events]



async def upsert_user(
    session: AsyncSession,
    telegram_id: int,
    first_name: str,
    last_name: str | None = None,
    username: str | None = None,
    user_role: str = UserRole.UNKNOWN
):
    stmt = upsert(User).values(
        {
            "telegram_id": telegram_id,
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "user_role": user_role
        }
    )
    stmt = stmt.on_conflict_do_update(
        index_elements=['telegram_id'],
        set_=dict(
            first_name=first_name,
            last_name=last_name,
            username=username,
        ),
    )
    await session.execute(stmt)
    await session.commit()

async def get_users_id(session: AsyncSession) -> list:
    stmt = select(User.telegram_id)
    result = await session.execute(stmt)
    return result.scalars().all()

async def get_users_by_role(session: AsyncSession, role: UserRole) -> list:
    stmt = select(User.telegram_id).where(User.user_role == role)
    result = await session.execute(stmt)
    return result.scalars().all()

async def get_users_exept_role(session: AsyncSession, role: UserRole) -> list:
    stmt = select(User.telegram_id).where(User.user_role != role)
    result = await session.execute(stmt)
    return result.scalars().all()

async def get_admins_id(session: AsyncSession) -> list:
    stmt = select(User.telegram_id).where(User.user_role == UserRole.ADMIN)
    result = await session.execute(stmt)
    return result.scalars().all()

async def get_super_admin_id(session: AsyncSession) -> list:
    stmt = select(User.telegram_id).where(User.user_role == UserRole.SUPER_ADMIN)
    result = await session.execute(stmt)
    return result.scalars().first()