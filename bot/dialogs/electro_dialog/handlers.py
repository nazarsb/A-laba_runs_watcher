from contextlib import suppress
from datetime import date
import logging
from dateutil.parser import parse

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ChatEvent
from aiogram_dialog.widgets.kbd import Button, Calendar
from aiogram_dialog.widgets.input import ManagedTextInput


from bot.dialogs.electro_dialog.states import ElectroSG
from bot.dialogs.start_dialog.states import StartSG
from bot.db_requests.db_requests import insert_event, get_users_exept_role
from database.enums.enums import UserRole


logger = logging.getLogger(__name__)


async def command_start_process(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data.update({'is_there_time': True})
    await dialog_manager.start(state=StartSG.start)

async def click_on_start_date(callback: ChatEvent, 
                              widget: Calendar, 
                              dialog_manager: DialogManager, 
                              selected_date: date, 
                              ):
    i18n = dialog_manager.middleware_data.get('i18n')
    if selected_date >= date.today():
        dialog_manager.dialog_data.update({'event_start_date': str(selected_date)})
        await dialog_manager.switch_to(state=ElectroSG.event_end_date)
    else:
        await callback.answer(text=i18n.get('calendar_warning', 
                                            selected_date=selected_date, 
                                            today=str(date.today())),
                              show_alert=True)


async def click_on_end_date(callback: ChatEvent, 
                            widget: Calendar, 
                            dialog_manager: DialogManager, 
                            selected_date: date, 
                            ):
    i18n = dialog_manager.middleware_data.get('i18n')
    start_date = date.fromisoformat(dialog_manager.dialog_data.get('event_start_date'))
    if selected_date >= start_date:
        dialog_manager.dialog_data.update({'event_end_date': str(selected_date)})
        await dialog_manager.switch_to(state=ElectroSG.event_time)
    else:
        await callback.answer(text=i18n.get('wrong_end_date', 
                                            start_date=dialog_manager.dialog_data.get('event_start_date'),
                                            selected_date=str(selected_date),
                                            ),
                              show_alert=True)


async def click_on_time1(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(state=ElectroSG.event_start_time)

async def click_on_time2(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(state=ElectroSG.summary)

def check_time(text: str):
    date_time = parse(text, dayfirst=True, fuzzy=True)
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
        error: ValueError,
        ):
    i18n = dialog_manager.middleware_data.get('i18n')
    await message.answer(
        text=i18n.get('wrong_time_format'),
    )

async def go_summary(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data.update({'time1': '','time2': '','is_there_time': False}) 
    await dialog_manager.switch_to(state=ElectroSG.summary)

async def go_back_from_summary(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    if dialog_manager.dialog_data.get('is_there_time') == False:
        await dialog_manager.switch_to(state=ElectroSG.event_time)
    else:
        await dialog_manager.switch_to(state=ElectroSG.event_end_time)

async def complete_new_event_plan(callback: CallbackQuery, 
                                  button: Button, 
                                  dialog_manager: DialogManager,
                                  ):
    i18n = dialog_manager.middleware_data.get('i18n')
    await insert_event(event_type_name=dialog_manager.start_data.get('event_type'),
                       event_name=dialog_manager.dialog_data.get('event_name'),
                       instrument_name=dialog_manager.dialog_data.get('instrument'),
                       reagent_name=dialog_manager.dialog_data.get('reagent'),
                       event_start_date=dialog_manager.dialog_data.get('event_start_date'),
                       event_end_date=dialog_manager.dialog_data.get('event_end_date'),
                       time_start=dialog_manager.dialog_data.get('time1'),
                       time_end=dialog_manager.dialog_data.get('time2'),
                       is_there_time=dialog_manager.dialog_data.get('is_there_time'),
                       session=dialog_manager.middleware_data.get('session'))
    bot = dialog_manager.middleware_data.get('bot')
    active_users = await get_users_exept_role(session=dialog_manager.middleware_data.get('session'), role=UserRole.UNKNOWN)
    for id in active_users:     # юзеров меньше 30, лимиты достичь невозможно, поэтому for порфовор.
        with suppress(BaseException):
            await bot.send_message(
                chat_id=id,
                text=i18n.get('electro_planned_notification',
                              event_start_date=dialog_manager.dialog_data.get('event_start_date'),
                              event_end_date=dialog_manager.dialog_data.get('event_end_date'),),
            )
    await dialog_manager.done()