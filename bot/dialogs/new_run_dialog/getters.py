
from aiogram_dialog import DialogManager
from sqlalchemy.ext.asyncio import AsyncSession
from fluentogram import TranslatorRunner

from bot.db_requests.db_requests import get_instrument_names, get_reagents


async def getter_instruments(session: AsyncSession, **kwargs):
    instruments = await get_instrument_names(session)
    return {'instruments': instruments}


async def getter_reagents(dialog_manager: DialogManager, session: AsyncSession, **kwargs):
    instrument = dialog_manager.dialog_data.get('instrument')
    reagents = await get_reagents(instrument, session)
    return {'reagents': reagents}


async def getter_summary(dialog_manager: DialogManager, 
                         i18n: TranslatorRunner, 
                         **kwargs):
    return {
            'is_qitan': True if dialog_manager.dialog_data.get('qitan_time') else False,
            'summary_keys': i18n.get('new_run_summary',
                event_type=dialog_manager.start_data.get('event_type'),
                instrument=dialog_manager.dialog_data.get('instrument'),
                run_start_date=dialog_manager.dialog_data.get('run_start_date'),
                ),
            'run_duration': i18n.get('new_run_duration',
                qitan_time=dialog_manager.dialog_data.get('qitan_time')),
            'reagent': i18n.get('new_run_reagent',
                reagent=dialog_manager.dialog_data.get('reagent'))
    }

