from aiogram.types import User
from aiogram_dialog import DialogManager
from sqlalchemy.ext.asyncio import AsyncSession


async def get_event_data(dialog_manager: DialogManager, **kwargs):
    name = dialog_manager.dialog_data.get('event_name')
    start_date = dialog_manager.dialog_data.get('event_start_date')
    end_date = dialog_manager.dialog_data.get('event_end_date')
    start_time = dialog_manager.dialog_data.get('event_start_time')
    end_time = dialog_manager.dialog_data.get('event_end_time')
    event_type = dialog_manager.start_data.get('event_type')
    is_there_time = dialog_manager.dialog_data.get('is_there_time')
    return {'event_name': name, 'event_start_date': start_date, 
            'event_end_date': end_date, 'event_start_time': start_time, 
            'event_end_time': end_time, 'event_type': event_type, 
            'is_there_time': is_there_time}