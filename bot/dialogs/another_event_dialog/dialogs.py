from aiogram.enums import ContentType

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format, Case, Multi
from aiogram_dialog.widgets.kbd import Button, Select, Calendar, Column, Group, Back, Next
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput, MessageInput

from bot.dialogs.another_event_dialog.getters import (get_another_event_end_date, get_another_event_start_date, 
                                                       get_another_event_start_time, get_another_event_end_time,
                                                       get_another_event_summary)
from bot.dialogs.another_event_dialog.states import AnotherEventSG
from bot.dialogs.another_event_dialog.handlers import (length_check, error_length_handler, 
                                                       correct_length_handler, no_text,
                                                       click_on_start_date, check_time,click_on_end_date,
                                                       error_time_handler, success_end_time_handler,
                                                       success_start_time_handler, go_summary, complete_new_event_plan)

from bot.dialogs.widgets.i18n import I18nFormat

another_event_dialog = Dialog(
    Window(
        I18nFormat('enter_another_event_name'),
        TextInput(
            id='event_name',
            type_factory=length_check,
            on_error=error_length_handler,
            on_success=correct_length_handler
        ),
        MessageInput(
            func=no_text,
            content_types=ContentType.ANY
        ),
        state=AnotherEventSG.event_name,
                  
    ),
    Window(
        Format('{another_event_start_date}'),
        Calendar(id='event_start_date',
                 on_click=click_on_start_date),
        Back(I18nFormat('back'), id='back'),
        state=AnotherEventSG.event_start_date,
        getter=get_another_event_start_date
    ),
    Window(
        Format('{another_event_start_time}'),
        TextInput(
            id='event_start_time',
            type_factory=check_time,
            on_success=success_start_time_handler,
            on_error=error_time_handler
        ),
        Next(I18nFormat('skip'), id='next'),
        Back(I18nFormat('back'), id='back'),
        state=AnotherEventSG.event_start_time,
        getter=get_another_event_start_time
    ),
    Window(
        Format('{another_event_end_date}'),
        Calendar(id='event_end_date',
                 on_click=click_on_end_date),
        Back(I18nFormat('back'), id='back'),
        state=AnotherEventSG.event_end_date,
        getter=get_another_event_end_date
    ),
    Window(
        Format('{another_event_end_time}'),
        TextInput(
            id='event_end_time',
            type_factory=check_time,
            on_success=success_end_time_handler,
            on_error=error_time_handler
        ),
        Button(I18nFormat('skip'), id='next', on_click=go_summary),
        Back(I18nFormat('back'), id='back'),
        state=AnotherEventSG.event_end_time,
        getter=get_another_event_end_time
    ),

    Window(
        I18nFormat('summary_pretext'),
        Case(
            texts={
                False:Format('{another_event_summary_wo_time}'),
                True: Format('{another_event_summary_with_time}'),
            },
            selector='is_there_time'
        ),
        Button(I18nFormat('yes'), id='complete', on_click=complete_new_event_plan),
        Back(I18nFormat('back'), id='back'),
        state=AnotherEventSG.summary,
        getter=get_another_event_summary

    ),
)