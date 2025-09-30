from aiogram.enums import ContentType

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format, Case, Multi
from aiogram_dialog.widgets.kbd import Button, Select, Calendar, Column, Group, Back, Next
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput, MessageInput

from bot.dialogs.another_event_dialog.getters import get_event_data
from bot.dialogs.another_event_dialog.states import AnotherEventSG
from bot.dialogs.another_event_dialog.handlers import (length_check, error_length_handler, 
                                                       correct_length_handler, no_text,
                                                       click_on_start_date, check_time,click_on_end_date,
                                                       error_time_handler, success_end_time_handler,
                                                       success_start_time_handler, go_summary, complete_new_event_plan)

another_event_dialog = Dialog(
    Window(
        Const('✍️ Введите название события'),
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
        Format('Планируем <u>{event_name}</u>'),
        Const('🗓 Выберите <b>дату начала</b> события'),
        Calendar(id='event_start_date',
                 on_click=click_on_start_date),
        Back(Const('Назад'), id='back'),
        state=AnotherEventSG.event_start_date,
    ),
    Window(
        Format('Планируем <u>{event_name}</u> на дату <u>{event_start_date}</u>'),
        Const('⏳ Введите <b>время начала</b> события или жмите "Пропустить"'),
        TextInput(
            id='event_start_time',
            type_factory=check_time,
            on_success=success_start_time_handler,
            on_error=error_time_handler
        ),
        Next(Const('Пропустить'), id='next'),
        Back(Const('Назад'), id='back'),
        state=AnotherEventSG.event_start_time,
    ),
    Window(
        Format('Планируем <u>{event_name}</u> на дату <u>{event_start_date}</u>'),
        Const('🗓 Выберите <b>дату окончания</b> события'),
        Calendar(id='event_end_date',
                 on_click=click_on_end_date),
        Back(Const('Назад'), id='back'),
        state=AnotherEventSG.event_end_date
    ),
    Window(
        Format('Планируем <u>{event_name}</u> на даты <u>{event_start_date} - {event_end_date}</u>'),
        Const('⌛️ Введите <b>время окончания</b> события или жмите "Пропустить"'),
        TextInput(
            id='event_end_time',
            type_factory=check_time,
            on_success=success_end_time_handler,
            on_error=error_time_handler
        ),
        Button(Const('Пропустить'), id='next', on_click=go_summary),
        Back(Const('Назад'), id='back'),
        state=AnotherEventSG.event_end_time
    ),

    Window(
        Const('📝 Краткое описание события'),
        Const('Если все <b>ОК</b>, жмите <b>"Да"</b>.\n'),
        Format('<b>Тип событие:</b> {event_type}'),
        Format('<b>Название события:</b> {event_name}'),
        Case(
            texts={
                True: Multi(
                    Format('<b>Начало события:</b> {event_start_date} {event_start_time}'),
                    Format('<b>Окончание события:</b> {event_end_date} {event_end_time}'),
                ),
                False: Multi(
                    Format('<b>Начало события:</b> {event_start_date}'),
                    Format('<b>Окончание события:</b> {event_end_date}'),
                ),
            },
            selector='is_there_time'
        ),
        Const('\nВсе верно?'),
        Button(Const('Да'), id='complete', on_click=complete_new_event_plan),
        Back(Const('Назад'), id='back'),
        state=AnotherEventSG.summary,
    ),
    getter=get_event_data
)