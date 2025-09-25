import logging

from aiogram.types import BotCommand
from fluentogram import TranslatorRunner

logger = logging.getLogger(__name__)


def get_main_menu_commands():
    menu_commands = {
        "/start": "✍️ Внести событие",
        "/show_events": "🗂 Показать события",
        "/cancel": "⛔️ Отмена",
    }
    main_menu_commands = [
        BotCommand(command=command, description=description)
        for command, description in menu_commands.items()
    ]
    return main_menu_commands