
import logging
from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button


logger = logging.getLogger(__name__)

router = Router(name='user_handlers')


async def go_back(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.back()

async def go_next(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.next()


