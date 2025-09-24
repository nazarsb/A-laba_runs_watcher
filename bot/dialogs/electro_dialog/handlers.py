from datetime import date

import logging

from dateutil.parser import parse

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, StartMode, ChatEvent
from aiogram_dialog.widgets.kbd import Button, Select, Calendar
from aiogram_dialog.widgets.input import ManagedTextInput, TextInput

from bot.dialogs.electro_dialog.states import ElectroSG
from bot.dialogs.start_dialog.states import StartSG
from bot.db_requests.db_requests import insert_event


logger = logging.getLogger(__name__)


async def command_start_process(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data.update({'is_there_time': True})
    await dialog_manager.start(state=StartSG.start)

async def click_on_start_date(callback: ChatEvent, widget: Calendar, dialog_manager: DialogManager, selected_date: date,):
    dialog_manager.dialog_data.update({'event_start_date': str(selected_date)})
    await dialog_manager.switch_to(state=ElectroSG.event_end_date)

async def click_on_end_date(callback: ChatEvent, widget: Calendar, dialog_manager: DialogManager, selected_date: date,):
    dialog_manager.dialog_data.update({'event_end_date': str(selected_date)})
    await dialog_manager.switch_to(state=ElectroSG.event_time)

async def click_on_time1(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(state=ElectroSG.event_start_time)

async def click_on_time2(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(state=ElectroSG.summary)

def check_time(text: str):
    date_time = parse(text, dayfirst=True)
    time = date_time.time() 
    if time:
        return {"time": time.strftime("%H:%M")}
    raise ValueError
    
async def success_time1_handler(
        message: Message, 
        widget: ManagedTextInput, 
        dialog_manager: DialogManager, 
        result: dict):
    dialog_manager.dialog_data.update({'time1': result.get('time')})
    await dialog_manager.switch_to(state=ElectroSG.event_end_time)

async def success_time2_handler(
        message: Message, 
        widget: ManagedTextInput, 
        dialog_manager: DialogManager, 
        result: dict):
    dialog_manager.dialog_data.update({'time2': result.get('time'),
                                       'is_there_time': True})
    await dialog_manager.switch_to(state=ElectroSG.summary)

async def error_time_handler(
        message: Message, 
        widget: ManagedTextInput, 
        dialog_manager: DialogManager, 
        error: ValueError):
    await message.answer(
        text='Вы ввели некорректный формат времени. Попробуйте еще раз.',
    )

async def go_summary(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data.update({'is_there_time': False})
    await dialog_manager.switch_to(state=ElectroSG.summary)


async def complete_new_event_plan(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await insert_event(event_type_name=dialog_manager.start_data.get('event_type'),
                       instrument_name=dialog_manager.dialog_data.get('instrument'),
                       reagent_name=dialog_manager.dialog_data.get('reagent'),
                       event_start_date=dialog_manager.dialog_data.get('event_start_date'),
                       event_end_date=dialog_manager.dialog_data.get('event_end_date'),
                       time_start=dialog_manager.dialog_data.get('time1'),
                       time_end=dialog_manager.dialog_data.get('time2'),
                       is_there_time=dialog_manager.dialog_data.get('is_there_time'),
                       session=dialog_manager.middleware_data.get('session'))
    await callback.answer('Событие запланировано. Просмотр событий - по команде /show_events', show_alert=True)
    await dialog_manager.done()