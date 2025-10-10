
from aiogram.types import User
from aiogram_dialog import DialogManager
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db_requests.db_requests import get_instrument_names, get_reagents


async def getter_instruments(session: AsyncSession, **kwargs):
    instruments = await get_instrument_names(session)
    return {'instruments': instruments}


async def getter_reagents(dialog_manager: DialogManager, session: AsyncSession, **kwargs):
    instrument = dialog_manager.dialog_data.get('instrument')
    reagents = await get_reagents(instrument, session)
    return {'reagents': reagents}


async def getter_summary(dialog_manager: DialogManager, **kwargs):
    return {'summary': dialog_manager.dialog_data, 
            'event_type': dialog_manager.start_data.get('event_type'),
            'is_qitan': True if dialog_manager.dialog_data.get('qitan_time') else False}