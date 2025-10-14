from aiogram.types import User
from aiogram_dialog import DialogManager
from sqlalchemy.ext.asyncio import AsyncSession
from fluentogram import TranslatorRunner


async def get_another_event_start_date(dialog_manager: DialogManager, 
                         i18n: TranslatorRunner, 
                         **kwargs):
    return {'another_event_start_date': i18n.get('another_event_start_date', 
                                   event_name=dialog_manager.dialog_data.get('event_name'))}

async def get_another_event_start_time(dialog_manager: DialogManager, 
                         i18n: TranslatorRunner, 
                         **kwargs):
    return {'another_event_start_time': i18n.get('another_event_start_time', 
                                   event_name=dialog_manager.dialog_data.get('event_name'),
                                   event_start_date=dialog_manager.dialog_data.get('event_start_date'))}
async def get_another_event_end_date(dialog_manager: DialogManager, 
                         i18n: TranslatorRunner, 
                         **kwargs):
    return {'another_event_end_date': i18n.get('another_event_end_date', 
                                   event_name=dialog_manager.dialog_data.get('event_name'),
                                   event_start_date=dialog_manager.dialog_data.get('event_start_date'))}

async def get_another_event_end_time(dialog_manager: DialogManager, 
                         i18n: TranslatorRunner, 
                         **kwargs):
    return {'another_event_end_time': i18n.get('another_event_end_time', 
                                   event_name=dialog_manager.dialog_data.get('event_name'),
                                   event_start_date=dialog_manager.dialog_data.get('event_start_date'),
                                   event_end_date=dialog_manager.dialog_data.get('event_end_date'))}

async def get_another_event_summary(dialog_manager: DialogManager, 
                         i18n: TranslatorRunner, 
                         **kwargs):
    return {'another_event_summary_wo_time': i18n.get('another_event_summary_wo_time',
                                   event_type=dialog_manager.start_data.get('event_type'), 
                                   event_name=dialog_manager.dialog_data.get('event_name'),
                                   event_start_date=dialog_manager.dialog_data.get('event_start_date'),
                                   event_end_date=dialog_manager.dialog_data.get('event_end_date'),),
            'another_event_summary_with_time': i18n.get('another_event_summary_with_time',
                                   event_type=dialog_manager.start_data.get('event_type'), 
                                   event_name=dialog_manager.dialog_data.get('event_name'),
                                   event_start_date=dialog_manager.dialog_data.get('event_start_date'),
                                   event_start_time=dialog_manager.dialog_data.get('event_start_time'),
                                   event_end_date=dialog_manager.dialog_data.get('event_end_date'),
                                   event_end_time=dialog_manager.dialog_data.get('event_end_time'),),
            'is_there_time': dialog_manager.dialog_data.get('is_there_time'),
            }   
