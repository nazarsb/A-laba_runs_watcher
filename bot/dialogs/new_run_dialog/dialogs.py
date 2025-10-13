from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format, Case
from aiogram_dialog.widgets.kbd import Button, Select, Calendar, Column, Group 
from aiogram_dialog.widgets.input import TextInput

from bot.dialogs.new_run_dialog.getters import getter_instruments, getter_reagents, getter_summary
from bot.dialogs.new_run_dialog.states import RunSG   
from bot.dialogs.new_run_dialog.handlers import (instrument_selection, click_on_date, reagent_selection, 
                                        complete_new_run_plan, go_back, command_start_process, success_qitantime_handler, 
                                        error_qitantime_handler, check_duration, switch_to_rundate, switch_to_duration_or_reagent)
from bot.dialogs.widgets.i18n import I18nFormat


new_run_dialog = Dialog(
    Window(
        I18nFormat('new_run_instruments'),
        Column(
        Select(
            Format('{item[0]}'),
            id='instr',
            item_id_getter=lambda x: x[1],
            items='instruments',
            on_click=instrument_selection,
        )),
        Button(I18nFormat('back'), id='back0', on_click=command_start_process),
        getter=getter_instruments,
        state=RunSG.new_run
    ),
    Window(
        I18nFormat('new_run_start_date'),
        Calendar(id='date', on_click=click_on_date),
        Button(I18nFormat('back'), id='back1', on_click=go_back),
        state=RunSG.run_date
    ),
    Window(
        I18nFormat('new_run_reagent_kit'),
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
            Button(I18nFormat('back'), id='back2', on_click=go_back),
        
            getter=getter_reagents,
            state=RunSG.reagent_kit
    ),
    Window(
        I18nFormat('new_run_duration'),
        TextInput(
            id='run_duration',
            type_factory=check_duration,
            on_success=success_qitantime_handler,
            on_error=error_qitantime_handler
        ),
        Button(I18nFormat('back'), id='to_run_date', on_click=switch_to_rundate),
        state=RunSG.run_duration
    ),  
    Window(
        I18nFormat('summary_pretext'),
        Format('{summary_keys}'),
        Case(
            texts={
                True: Format('{run_duration}'),
                False: Format('{reagent}'),
            },
            selector='is_qitan'
        ),
        Button(I18nFormat('complete'), id='complete', on_click=complete_new_run_plan),
        Button(I18nFormat('back'), id='either_duration_or_reagent', on_click=switch_to_duration_or_reagent),
        getter=getter_summary,
        state=RunSG.summary
    ),
)
