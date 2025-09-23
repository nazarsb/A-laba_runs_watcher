from datetime import date

import logging
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, StartMode, ChatEvent
from aiogram_dialog.widgets.kbd import Button, Select, Calendar

from bot.dialogs.new_run_dialog.states import RunSG
from bot.dialogs.start_dialog.states import StartSG

logger = logging.getLogger(__name__)


async def go_back(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.back()

async def go_next(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.next()

async def command_start_process(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(state=StartSG.start)

async def click_new_run(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data.update({'event_type': str(callback['data'])})
    await dialog_manager.start(state=RunSG.new_run)

async def instrument_selection(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, selected_instrument: str):
    dialog_manager.dialog_data.update({'instrument': selected_instrument})
    await dialog_manager.switch_to(state=RunSG.run_date)

async def click_on_date(callback: ChatEvent, widget: Calendar, dialog_manager: DialogManager, selected_date: date,):
    dialog_manager.dialog_data.update({'run_date': str(selected_date)})
    await dialog_manager.switch_to(state=RunSG.reagent_kit)

async def reagent_selection(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, selected_reagent: str):
    dialog_manager.dialog_data.update({'reagent': selected_reagent})
    await dialog_manager.switch_to(state=RunSG.summary)

async def complete_new_run_plan(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await callback.answer('Событие запланировано. Просмотр событий - по команде /show_events', show_alert=True)
    await dialog_manager.done()
