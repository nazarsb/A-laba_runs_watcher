from contextlib import suppress
from datetime import date, datetime, timedelta

import logging
from aiogram import Bot, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, StartMode, ChatEvent
from aiogram_dialog.widgets.kbd import Button, Select, Calendar

from database.enums.enums import UserRole
from sqlalchemy.ext.asyncio import AsyncSession

from bot.dialogs.new_run_dialog.states import RunSG
from bot.dialogs.start_dialog.states import StartSG
from bot.db_requests.db_requests import get_users_exept_role, insert_event, get_runtime

logger = logging.getLogger(__name__)


async def go_back(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.back()

async def go_next(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.next()

async def command_start_process(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(state=StartSG.start)

async def click_new_run(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(state=RunSG.new_run)

async def instrument_selection(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, selected_instrument: str):
    dialog_manager.dialog_data.update({'instrument': selected_instrument,
                                       'is_there_time': False})
    await dialog_manager.switch_to(state=RunSG.run_date)

async def click_on_date(callback: ChatEvent, widget: Calendar, dialog_manager: DialogManager, selected_date: date,):
    dialog_manager.dialog_data.update({'run_start_date': str(selected_date)})
    await dialog_manager.switch_to(state=RunSG.reagent_kit)

async def reagent_selection(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, selected_reagent: str):
    run_duration = await get_runtime(selected_reagent, dialog_manager.middleware_data.get('session'))
    run_start_date = dialog_manager.dialog_data.get('run_start_date')
    dialog_manager.dialog_data.update({'reagent': selected_reagent,
                                       'run_end_date': (datetime.strptime(run_start_date, '%Y-%m-%d') + timedelta(hours=run_duration+12)).strftime('%Y-%m-%d')})
    await dialog_manager.switch_to(state=RunSG.summary)

async def complete_new_run_plan(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await insert_event(event_type_name=dialog_manager.start_data.get('event_type'),
                       instrument_name=dialog_manager.dialog_data.get('instrument'),
                       reagent_name=dialog_manager.dialog_data.get('reagent'),
                       event_start_date=dialog_manager.dialog_data.get('run_start_date'),
                       event_end_date=dialog_manager.dialog_data.get('run_end_date'),
                       time_start=dialog_manager.dialog_data.get('time1'),
                       time_end=dialog_manager.dialog_data.get('time2'),
                       is_there_time=dialog_manager.dialog_data.get('is_there_time'),
                       session=dialog_manager.middleware_data.get('session'))
    await callback.answer('Событие запланировано. Просмотр событий - по команде /show_events', show_alert=True)
    bot = dialog_manager.middleware_data.get('bot')
    active_users = await get_users_exept_role(session=dialog_manager.middleware_data.get('session'), role=UserRole.UNKNOWN)
    for id in active_users:
        with suppress(BaseException):
            await bot.send_message(
                chat_id=id,
                text=f'🚀 Запланирован новый <b>запуск</b> на <b>{dialog_manager.dialog_data.get("run_start_date")} - {dialog_manager.dialog_data.get("run_end_date")}</b>. \
                \nПросмотр событий - по команде \n<b>/show_events</b>'
            )
    await dialog_manager.done()
