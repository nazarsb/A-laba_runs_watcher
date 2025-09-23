
from aiogram.types import User
from aiogram_dialog import DialogManager
 


async def getter_instruments(**kwargs):
    instruments = [
        ('NovaSeq 6000', 'NovaSeq 6000'),
        ('Salus Pro', 'Salus Pro'),
        ('Salus Evo', 'Salus Evo'),
    ]
    return {'instruments': instruments}


async def getter_reagents(dialog_manager: DialogManager, **kwargs):
    if dialog_manager.dialog_data.get('instrument') == 'NovaSeq 6000':
        reagents = [
            ('S1 300', 'S1 300'),
            ('S4 300', 'S4 300'),
           
        ]
    elif dialog_manager.dialog_data.get('instrument') == 'Salus Pro':
        reagents = [
            ('80M PE100', '80M PE300'),
            ('300M PE100', '300M PE100'),
        ]
    elif dialog_manager.dialog_data.get('instrument') == 'Salus Evo':
        reagents = [
            ('1500M PE100', '1500M PE100'),
            ('3000M PE100', '3000M PE100'),
        ]
    return {'reagents': reagents}


async def getter_summary(dialog_manager: DialogManager, **kwargs):
    return {'summary': dialog_manager.dialog_data, 
            'event_type': dialog_manager.start_data.get('event_type')}