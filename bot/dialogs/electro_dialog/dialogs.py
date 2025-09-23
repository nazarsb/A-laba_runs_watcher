from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format, Case, Multi
from aiogram_dialog.widgets.kbd import (Button, Calendar, Back)
from aiogram_dialog.widgets.input import TextInput

from bot.dialogs.electro_dialog.handlers import (click_on_start_date, click_on_end_date, 
                                                 command_start_process, complete_new_event_plan, 
                                                 click_on_time1, check_time, error_time_handler, success_time1_handler,
                                                 success_time2_handler, go_summary)
from bot.dialogs.electro_dialog.states import ElectroSG
from bot.dialogs.electro_dialog.getters import get_event_dates_time




electro_dialog = Dialog(
    Window(
        Const('В какой день <b>начало</b> отключения?'),
        Calendar(id='date1', on_click=click_on_start_date),
        Button(Const('Назад'), id='back1', on_click=command_start_process),
        state=ElectroSG.event_start_date
    ),

    Window(
        Format('Начало отключения: {event_start_date}'),
        Const('А в какой дадут электричество?'),
        Calendar(id='date2', on_click=click_on_end_date),
        Back(Const('Назад'), id='back2'),
        state=ElectroSG.event_end_date,
    ),

    Window(
        Format('Отключение будет в дни: {event_start_date} - {event_end_date}'),
        Const('Хотите указать конкретное время отключения?'),
        Button(Const('Да'), id='time1', on_click=click_on_time1),
        Button(Const('Нет'), id='time2', on_click=go_summary),
        Back(Const('Назад'), id='back3'),
        state=ElectroSG.event_time,
    ),

    Window(
        Format('Отключение будет в дни: <b>{event_start_date} - {event_end_date}</b>'),
        Const('Введите время <b>НАЧАЛА</b> отключения'),
        Const('<b><i>Формат - ЧЧ:ММ</i></b>'),
        TextInput(id='time1',
                  type_factory=check_time,
                  on_success=success_time1_handler,
                  on_error=error_time_handler),
        Back(Const('Назад'), id='back4'),
        state=ElectroSG.event_start_time,
    ),

    Window(
        Format('Отключение будет в дни: <b>{event_start_date} - {event_end_date}</b>'),
        Format('Время начала отключения: <b>{time1}</b>'),
        Const('В какое время <b>ОКОНЧАНИЯ</b> отключения?'),
        Const('<b><i>Формат - ЧЧ:ММ</i></b>'),
        TextInput(id='time2',
                  type_factory=check_time,
                  on_success=success_time2_handler,
                  on_error=error_time_handler),
        Back(Const('Назад'), id='back5'),
        state=ElectroSG.event_end_time,
    ),

    Window(
        Format('<b>Тип события:</b> {event_type}\n'),
        Case(
            texts={
                True : Multi(
                    Format('<b>Начало отключения:</b> {event_start_date} в {time1}'),
                    Format('<b>Конец отключения:</b> {event_end_date} в {time2}'),
                    Const('\nВсе верно?')
                ),
                False: Multi(
                    Format('<b>Начало отключения:</b> {event_start_date}'),
                    Format('<b>Конец отключения:</b> {event_end_date}'),
                    Const('\nВсе верно?')
                )
            },
            selector='is_there_time',
        ),
        Button(Const('Да'), id='complete', on_click=complete_new_event_plan),
        Back(Const('Назад'), id='back6'),
        state=ElectroSG.summary
    ),
    getter=get_event_dates_time
)
