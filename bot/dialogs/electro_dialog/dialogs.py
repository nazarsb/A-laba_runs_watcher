from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format, Case
from aiogram_dialog.widgets.kbd import (Button, Calendar, Back)
from aiogram_dialog.widgets.input import TextInput

from bot.dialogs.electro_dialog.handlers import (click_on_start_date, click_on_end_date, 
                                                 command_start_process, complete_new_event_plan, 
                                                 click_on_time1, check_time, error_time_handler, success_time1_handler,
                                                 success_time2_handler, go_summary, go_back_from_summary)
from bot.dialogs.electro_dialog.states import ElectroSG
from bot.dialogs.electro_dialog.getters import (get_summary, get_event_dates, 
                                                get_event_is_time, get_event_start_time,
                                                get_event_end_time)
from bot.dialogs.widgets.i18n import I18nFormat




electro_dialog = Dialog(
    Window(
        I18nFormat('electro_start_date'),
        Calendar(id='date1', on_click=click_on_start_date),
        Button(I18nFormat('back'), id='back1', on_click=command_start_process),
        state=ElectroSG.event_start_date
    ),

    Window(
        Format('{electro_end_date}'),
        Calendar(id='date2', on_click=click_on_end_date),
        Back(I18nFormat('back'), id='back2'),
        state=ElectroSG.event_end_date,
        getter=get_event_dates
    ),

    Window(
        Format('{is_time_question}'),
        Button(I18nFormat('yes'), id='yes', on_click=click_on_time1),
        Button(I18nFormat('no'), id='no', on_click=go_summary),
        Back(I18nFormat('back'), id='back3'),
        state=ElectroSG.event_time,
        getter=get_event_is_time
    ),

    Window(
        Format('{elcetro_start_time}'),
        TextInput(id='time1',
                  type_factory=check_time,
                  on_success=success_time1_handler,
                  on_error=error_time_handler),
        Back(I18nFormat('back'), id='back4'),
        state=ElectroSG.event_start_time,
        getter=get_event_start_time
    ),

    Window(
        Format('{electro_end_time}'),
        TextInput(id='time2',
                  type_factory=check_time,
                  on_success=success_time2_handler,
                  on_error=error_time_handler),
        Back(I18nFormat('back'), id='back5'),
        state=ElectroSG.event_end_time,
        getter=get_event_end_time
    ),

    Window(
        I18nFormat('summary_pretext'),
        Case(
            texts={
                True : Format('{electro_summary_with_time}'),
                False: Format('{electro_summary_wo_time}'),
            },
            selector='is_there_time',
        ),
        Button(I18nFormat('yes'), id='complete', on_click=complete_new_event_plan),
        Button(I18nFormat('back'), id='back_frm_sum', on_click=go_back_from_summary),
        state=ElectroSG.summary,
        getter=get_summary
    ),
)
