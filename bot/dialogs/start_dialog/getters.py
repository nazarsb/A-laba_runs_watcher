from aiogram.types import User
from aiogram_dialog import DialogManager
 

async def getter_user(dialog_manager: DialogManager, event_from_user: User, **kwargs):  
    if dialog_manager.start_data:
        getter_user_data = {
        'name': event_from_user.first_name,
        'is_first': True
        }
        dialog_manager.start_data.clear()
    else:
        getter_user_data = {'is_first': False}    
    return getter_user_data