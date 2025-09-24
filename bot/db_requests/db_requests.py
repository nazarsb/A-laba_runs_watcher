import logging

from sqlalchemy import case, func, insert, literal, select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update

from database.models import Event, Instrument, Reagent


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