from aiogram.types import User
from aiogram_dialog import DialogManager


async def get_event_dates_time(dialog_manager: DialogManager, **kwargs):
    return {'event_start_date': dialog_manager.dialog_data.get('event_start_date'),
            'event_end_date': dialog_manager.dialog_data.get('event_end_date'),
            'time1': dialog_manager.dialog_data.get('time1'),
            'time2': dialog_manager.dialog_data.get('time2'),
            'is_there_time': dialog_manager.dialog_data.get('is_there_time'),
            'event_type': dialog_manager.start_data.get('event_type')}