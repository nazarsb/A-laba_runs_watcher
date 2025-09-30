from datetime import date

import logging
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, StartMode, ChatEvent
from aiogram_dialog.widgets.kbd import Button, Select, Calendar

from bot.dialogs.start_dialog.states import StartSG
from bot.dialogs.new_run_dialog.states import RunSG
from bot.dialogs.electro_dialog.states import ElectroSG
from bot.dialogs.another_event_dialog.states import AnotherEventSG

logger = logging.getLogger(__name__)

router = Router(name='user_handlers')


async def go_back(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.back()

async def go_next(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.next()

async def click_new_run(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(state=RunSG.new_run, data={'event_type': 'Запуск прибора'})

async def click_new_event(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(state=ElectroSG.event_start_date, data={'event_type': 'Отключение энергии'})

async def click_alother_event(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(state=AnotherEventSG.event_name, data={'event_type': 'Другое событие'})
    # await callback.answer(text='Этот раздел еще в разработке. Обождите.', show_alert=True)
