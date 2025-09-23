from datetime import date

import logging
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, StartMode, ChatEvent
from aiogram_dialog.widgets.kbd import Button, Select, Calendar

from bot.dialogs.start_dialog.states import StartSG

logger = logging.getLogger(__name__)

router = Router(name='user_handlers')

@router.message(CommandStart())
async def command_start_process(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK)