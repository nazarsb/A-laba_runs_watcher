from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format, Case
from aiogram_dialog.widgets.kbd import Button, Select, Calendar, Column, Group 
from aiogram_dialog.widgets.input import TextInput

from bot.dialogs.new_run_dialog.getters import getter_instruments, getter_reagents, getter_summary
from bot.dialogs.new_run_dialog.states import RunSG   
from bot.dialogs.new_run_dialog.handlers import (instrument_selection, click_on_date, reagent_selection, 
                                        complete_new_run_plan, go_back, command_start_process, success_qitantime_handler, 
                                        error_qitantime_handler, check_duration, switch_to_rundate, switch_to_duration_or_reagent)



new_run_dialog = Dialog(
    Window(
        Const('На каком <b>приборе</b> запускаемся?'),
        Column(
        Select(
            Format('{item[0]}'),
            id='instr',
            item_id_getter=lambda x: x[1],
            items='instruments',
            on_click=instrument_selection,
        )),
        Button(Const('Назад'), id='back0', on_click=command_start_process),
        getter=getter_instruments,
        state=RunSG.new_run
    ),
    Window(
        Const('Дата <b>НАЧАЛА</b> запуска'),
        Calendar(id='date', on_click=click_on_date),
        Button(Const('Назад'), id='back1', on_click=go_back),
        state=RunSG.run_date
    ),
    Window(
        Const('Какой <b>набор</b> будем использовать? \n\n<i>на основании этого бот сам посчитает длительность запуска 🤓</i>'),
        Group(
        Column(
            Select(
                Format('{item[0]}'),
                id='reagent',
                item_id_getter=lambda x: x[1],
                items='reagents',
                on_click=reagent_selection,
            )),
            width=3
        ),
            Button(Const('Назад'), id='back2', on_click=go_back),
        
            getter=getter_reagents,
            state=RunSG.reagent_kit
    ),
    Window(
        Const('Введите длительность запуска <u><b>в часах</b></u>.'),
        TextInput(
            id='run_duration',
            type_factory=check_duration,
            on_success=success_qitantime_handler,
            on_error=error_qitantime_handler
        ),
        Button(Const('Назад'), id='to_run_date', on_click=switch_to_rundate),
        state=RunSG.run_duration
    ),  
    Window(
        Const('📝 Краткое описание события'),
        Const('Если все <b>ОК</b>, жмите <b>"Завершить"</b>.\n'),
        Format('<b>Запланированное событие:</b> {event_type}'),
        Format('<b>Инструмент:</b> {summary[instrument]}'),
        Format('<b>Дата запуска:</b> {summary[run_start_date]}'),
        Case(
            texts={
                True: Format('<b>Длительность запуска:</b> {summary[qitan_time]} ч.'),
                False: Format('<b>Реагент:</b> {summary[reagent]}'),
            },
            selector='is_qitan'
        ),
        Button(Const('Завершить'), id='complete', on_click=complete_new_run_plan),
        Button(Const('Назад'), id='either_duration_or_reagent', on_click=switch_to_duration_or_reagent),
        getter=getter_summary,
        state=RunSG.summary
    ),
)
