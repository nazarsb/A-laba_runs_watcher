from contextlib import suppress
from datetime import date
import logging
from dateutil.parser import parse

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ChatEvent
from aiogram_dialog.widgets.kbd import Button, Calendar
from aiogram_dialog.widgets.input import ManagedTextInput, MessageInput

from bot.dialogs.another_event_dialog.states import AnotherEventSG
from bot.db_requests.db_requests import insert_event, get_users_exept_role
from database.enums.enums import UserRole

logger = logging.getLogger(__name__)

def length_check(text: str) -> str:
    if 2 <= len(text) <= 64:
        return text
    raise ValueError

async def error_length_handler(
        message: Message, 
        widget: ManagedTextInput, 
        dialog_manager: DialogManager, 
        error: ValueError):
    await message.answer(
        text='Название должно быть от 2 до 64 символов. Попробуйте еще раз'
    )

async def no_text(message: Message, widget: MessageInput, dialog_manager: DialogManager):
    await message.answer(text='Нужно ввести текст с названием события. Попробуйте еще раз')

async def correct_length_handler(
        message: Message, 
        widget: ManagedTextInput, 
        dialog_manager: DialogManager, 
        text: str) -> None:
    dialog_manager.dialog_data.update({'event_name': text})
    await dialog_manager.switch_to(AnotherEventSG.event_start_date)

async def click_on_start_date(callback: ChatEvent, widget: Calendar, dialog_manager: DialogManager, selected_date: date,):
    if selected_date >= date.today():
        dialog_manager.dialog_data.update({'event_start_date': str(selected_date)})
        await dialog_manager.switch_to(state=AnotherEventSG.event_start_time)
    else:
        await callback.answer(text=f'{selected_date} уже в прошлом.\nСегодня уже {str(date.today())}. \nВыберете актуальную дату.', 
                              show_alert=True)

def check_time(text: str):
    date_time = parse(text, dayfirst=True)
    time = date_time.time() 
    if time:
        return {"time": time.strftime("%H:%M")}
    raise ValueError

async def error_time_handler(
        message: Message, 
        widget: ManagedTextInput, 
        dialog_manager: DialogManager, 
        error: ValueError):
    i18n = dialog_manager.middleware_data.get('i18n')
    await message.answer(
        text=i18n.get('wrong_time_format'),
    )

async def success_start_time_handler(
        message: Message, 
        widget: ManagedTextInput, 
        dialog_manager: DialogManager, 
        result: dict):
    dialog_manager.dialog_data.update({'event_start_time': result.get('time'), 
                                       'is_there_time': True})
    await dialog_manager.switch_to(state=AnotherEventSG.event_end_date)

async def click_on_end_date(callback: ChatEvent, widget: Calendar, dialog_manager: DialogManager, selected_date: date,):
    i18n = dialog_manager.middleware_data.get('i18n')
    start_date = date.fromisoformat(dialog_manager.dialog_data.get('event_start_date'))
    if selected_date >= start_date:
        dialog_manager.dialog_data.update({'event_end_date': str(selected_date)})
        await dialog_manager.switch_to(state=AnotherEventSG.event_end_time)
    else:
        await callback.answer(text=i18n.get('wrong_end_date', 
                                            start_date=dialog_manager.dialog_data.get('event_start_date'),
                                            selected_date=selected_date.strftime('%Y-%m-%d'),), 
                            show_alert=True)

async def success_end_time_handler(
        message: Message, 
        widget: ManagedTextInput,   
        dialog_manager: DialogManager, 
        result: dict):
    dialog_manager.dialog_data.update({'event_end_time': result.get('time'),
                                       'is_there_time': True})
    await dialog_manager.switch_to(state=AnotherEventSG.summary)

async def go_summary(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data.update({'event_start_time': '', 'event_end_time': '', 'is_there_time': False})
    await dialog_manager.switch_to(state=AnotherEventSG.summary)

async def complete_new_event_plan(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await insert_event(event_type_name=dialog_manager.start_data.get('event_type'),
                       event_name=dialog_manager.dialog_data.get('event_name'),
                       instrument_name=dialog_manager.dialog_data.get('instrument'),
                       reagent_name=dialog_manager.dialog_data.get('reagent'),
                       event_start_date=dialog_manager.dialog_data.get('event_start_date'),
                       event_end_date=dialog_manager.dialog_data.get('event_end_date'),
                       time_start=dialog_manager.dialog_data.get('event_start_time'),
                       time_end=dialog_manager.dialog_data.get('event_end_time'),
                       is_there_time=dialog_manager.dialog_data.get('is_there_time'),
                       session=dialog_manager.middleware_data.get('session'))
    bot = dialog_manager.middleware_data.get('bot')
    i18n = dialog_manager.middleware_data.get('i18n')
    active_users = await get_users_exept_role(session=dialog_manager.middleware_data.get('session'), role=UserRole.UNKNOWN)
    for id in active_users:    # юзеров меньше 30, лимиты достичь невозможно, поэтому for порфовор.
        with suppress(BaseException):
            await bot.send_message(
                chat_id=id,
                text=i18n.get('another_event_planned_notification', 
                             event_name=dialog_manager.dialog_data.get('event_name'),
                             event_start_date=dialog_manager.dialog_data.get('event_start_date'),
                             event_end_date=dialog_manager.dialog_data.get('event_end_date'),
                ),
            )
    await dialog_manager.done()






