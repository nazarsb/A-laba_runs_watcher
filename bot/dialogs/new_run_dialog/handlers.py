from contextlib import suppress
from datetime import date, datetime, timedelta

import logging
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ChatEvent
from aiogram_dialog.widgets.kbd import Button, Select, Calendar
from aiogram_dialog.widgets.input import ManagedTextInput

from database.enums.enums import UserRole

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

async def click_on_date(callback: ChatEvent, 
                        widget: Calendar, 
                        dialog_manager: DialogManager, 
                        selected_date: date):
    i18n = dialog_manager.middleware_data.get('i18n')
    if selected_date >= date.today():
        dialog_manager.dialog_data.update({'run_start_date': str(selected_date)})
        if dialog_manager.dialog_data.get('instrument') in ('Qnome-3841',):
            await dialog_manager.switch_to(state=RunSG.run_duration)
        else:
            await dialog_manager.switch_to(state=RunSG.reagent_kit)
    else:
        await callback.answer(text=i18n.get('calendar_warning', selected_date=selected_date, today=str(date.today())),
                              show_alert=True)



def check_duration(text: str): 
    if 1 <= int(text) <= 72:
        return {"run_duration": int(text)}
    raise ValueError


async def success_qitantime_handler(
        message: Message, 
        widget: ManagedTextInput, 
        dialog_manager: DialogManager, 
        result: dict):
    dialog_manager.dialog_data.update({'qitan_time': result.get('run_duration')})
    run_start_date = dialog_manager.dialog_data.get('run_start_date')
    dialog_manager.dialog_data.update({'run_end_date': (datetime.strptime(run_start_date, '%Y-%m-%d') + timedelta(hours=result.get('run_duration'))).strftime('%Y-%m-%d')})
    await dialog_manager.switch_to(state=RunSG.summary)

async def error_qitantime_handler(
        message: Message, 
        widget: ManagedTextInput, 
        dialog_manager: DialogManager, 
        error: ValueError):
    i18n = dialog_manager.middleware_data.get('i18n')
    await message.answer(text=i18n.get('wrong_duration_frmt'))
    


async def switch_to_rundate(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(state=RunSG.run_date)


async def switch_to_duration_or_reagent(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    if not dialog_manager.dialog_data.get('qitan_time'):
        await dialog_manager.switch_to(state=RunSG.reagent_kit)
    else:
        await dialog_manager.switch_to(state=RunSG.run_duration)
        dialog_manager.dialog_data.pop('qitan_time')


async def reagent_selection(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, selected_reagent: str):
    run_duration = await get_runtime(selected_reagent, dialog_manager.middleware_data.get('session'))
    run_start_date = dialog_manager.dialog_data.get('run_start_date')
    dialog_manager.dialog_data.update({'reagent': selected_reagent,
                                       'run_end_date': (datetime.strptime(run_start_date, '%Y-%m-%d') + timedelta(hours=run_duration+12)).strftime('%Y-%m-%d')})
    await dialog_manager.switch_to(state=RunSG.summary)


async def complete_new_run_plan(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await insert_event(event_type_name=dialog_manager.start_data.get('event_type'),
                       event_name=dialog_manager.dialog_data.get('event_name'),
                       instrument_name=dialog_manager.dialog_data.get('instrument'),
                       reagent_name=dialog_manager.dialog_data.get('reagent'),
                       event_start_date=dialog_manager.dialog_data.get('run_start_date'),
                       event_end_date=dialog_manager.dialog_data.get('run_end_date'),
                       time_start=dialog_manager.dialog_data.get('time1'),
                       time_end=dialog_manager.dialog_data.get('time2'),
                       is_there_time=dialog_manager.dialog_data.get('is_there_time'),
                       session=dialog_manager.middleware_data.get('session'))
    bot = dialog_manager.middleware_data.get('bot')
    active_users = await get_users_exept_role(session=dialog_manager.middleware_data.get('session'), role=UserRole.UNKNOWN)
    i18n = dialog_manager.middleware_data.get('i18n')
    for id in active_users:         # юзеров меньше 30, лимиты достичь невозможно, поэтому for порфовор.
        with suppress(BaseException):
            await bot.send_message(
                chat_id=id,
                text=i18n.get('new_run_planned_notification',
                              run_start_date=dialog_manager.dialog_data.get("run_start_date"),
                              run_end_date=dialog_manager.dialog_data.get("run_end_date"),),
            )
    await dialog_manager.done()


