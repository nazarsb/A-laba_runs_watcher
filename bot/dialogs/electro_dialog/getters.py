from aiogram.types import User
from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner


async def get_event_dates_time(dialog_manager: DialogManager, 
                               i18n: TranslatorRunner, 
                               **kwargs):
    return {'event_start_date': dialog_manager.dialog_data.get('event_start_date'),
            'is_there_time': dialog_manager.dialog_data.get('is_there_time'),
            'event_end_date': dialog_manager.dialog_data.get('event_end_date'),
            'time1': dialog_manager.dialog_data.get('time1'),
            'time2': dialog_manager.dialog_data.get('time2'),
            'electro_start_date': i18n.get('electro_start_date'),
            
            
            'electro_start_time': i18n.get('electro_start_time',
                                           event_start_date=dialog_manager.dialog_data.get('event_start_date'),
                                           event_end_date=dialog_manager.dialog_data.get('event_end_date'),),
            'electro_end_time': i18n.get('electro_end_time',
                                         event_start_date=dialog_manager.dialog_data.get('event_start_date'),
                                         event_end_date=dialog_manager.dialog_data.get('event_end_date'),
                                         time1=dialog_manager.dialog_data.get('time1'),),
            'electro_summary_with_time': i18n.get('electro_summary_with_time',
                                                  event_type=dialog_manager.start_data.get('event_type'),
                                                  event_start_date=dialog_manager.dialog_data.get('event_start_date'),
                                                  event_end_date=dialog_manager.dialog_data.get('event_end_date'),
                                                  time1=dialog_manager.dialog_data.get('time1'),
                                                  time2=dialog_manager.dialog_data.get('time2'),),
            'electro_summary_wo_time': i18n.get('electro_summary_wo_time',
                                                event_type=dialog_manager.start_data.get('event_type'),
                                                event_start_date=dialog_manager.dialog_data.get('event_start_date'),
                                                event_end_date=dialog_manager.dialog_data.get('event_end_date'),),
            'electro_end_date': i18n.get('electro_end_date', 
                                     event_start_date=dialog_manager.dialog_data.get('event_start_date'),),
            }

async def get_event_dates(dialog_manager: DialogManager, 
                               i18n: TranslatorRunner, 
                               **kwargs):
    return {'event_start_date': dialog_manager.dialog_data.get('event_start_date'),
            'electro_end_date': i18n.get('electro_end_date', 
                                         event_start_date=dialog_manager.dialog_data.get('event_start_date')),}
async def get_event_is_time(dialog_manager: DialogManager, 
                               i18n: TranslatorRunner, 
                               **kwargs):
    return {'is_time_question': i18n.get('do_enter_time', 
                                         event_start_date=dialog_manager.dialog_data.get('event_start_date'),
                                         event_end_date=dialog_manager.dialog_data.get('event_end_date'),),}
async def get_event_start_time(dialog_manager: DialogManager, 
                               i18n: TranslatorRunner, 
                               **kwargs):
    return {'elcetro_start_time': i18n.get('elcetro_start_time',
                                           event_start_date=dialog_manager.dialog_data.get('event_start_date'),
                                           event_end_date=dialog_manager.dialog_data.get('event_end_date'),),
            }
async def get_event_end_time(dialog_manager: DialogManager, 
                               i18n: TranslatorRunner, 
                               **kwargs):
    return {'electro_end_time': i18n.get('electro_end_time',
                                         event_start_date=dialog_manager.dialog_data.get('event_start_date'),
                                         event_end_date=dialog_manager.dialog_data.get('event_end_date'),
                                         time1=dialog_manager.dialog_data.get('time1'),),}
async def get_summary(dialog_manager: DialogManager, 
                               i18n: TranslatorRunner, 
                               **kwargs):
    return {'electro_summary_with_time': i18n.get('electro_summary_with_time',
                                                  event_type=dialog_manager.start_data.get('event_type'),
                                                  event_start_date=dialog_manager.dialog_data.get('event_start_date'),
                                                  event_end_date=dialog_manager.dialog_data.get('event_end_date'),
                                                  time1=dialog_manager.dialog_data.get('time1'),
                                                  time2=dialog_manager.dialog_data.get('time2')),
            'electro_summary_wo_time': i18n.get('electro_summary_wo_time',
                                                event_type=dialog_manager.start_data.get('event_type'),
                                                event_start_date=dialog_manager.dialog_data.get('event_start_date'),
                                                event_end_date=dialog_manager.dialog_data.get('event_end_date')),
            'is_there_time': dialog_manager.dialog_data.get('is_there_time'),
    }