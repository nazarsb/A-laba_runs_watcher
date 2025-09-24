from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Select, Calendar, Column

from bot.dialogs.new_run_dialog.getters import getter_instruments, getter_reagents, getter_summary
from bot.dialogs.new_run_dialog.states import RunSG   
from bot.dialogs.new_run_dialog.handlers import (click_new_run, instrument_selection, click_on_date, reagent_selection, 
                                        complete_new_run_plan, go_back, command_start_process)



new_run_dialog = Dialog(
    Window(
        Const('На каком приборе запускаемся?'),
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
        Const('Дата запуска'),
        Calendar(id='date', on_click=click_on_date),
        Button(Const('Назад'), id='back1', on_click=go_back),
        state=RunSG.run_date
    ),
    Window(
        Const('Какой реагент использовать?'),
        Column(
            Select(
                Format('{item[0]}'),
                id='reagent',
                item_id_getter=lambda x: x[1],
                items='reagents',
                on_click=reagent_selection,
            ),
            Button(Const('Назад'), id='back2', on_click=go_back),
        ),
            getter=getter_reagents,
            state=RunSG.reagent_kit
    ),
    Window(
        Const('Краткое описание события'),
        Const('Если все ОК, жмите "Завершить".\n'),
        Format('<b>Запланированное событие:</b> {event_type}'),
        Format('<b>Инструмент:</b> {summary[instrument]}'),
        Format('<b>Дата запуска:</b> {summary[run_start_date]}'),
        Format('<b>Реагент:</b> {summary[reagent]}'),
        Button(Const('Назад'), id='back3', on_click=go_back),
        Button(Const('Завершить'), id='complete', on_click=complete_new_run_plan),
        getter=getter_summary,
        state=RunSG.summary
    ),
)
