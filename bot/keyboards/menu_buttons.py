import logging

from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeAllPrivateChats, BotCommandScopeAllGroupChats

from aiogram.types import BotCommand

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


async def menu_set_up(bot: Bot):
    logger.info("Starting bot... Setting up default commands.")
    await bot.set_my_commands(get_main_menu_commands(), BotCommandScopeAllPrivateChats())

async def menu_drop_down(bot: Bot):
    logger.info("Bot stopping... Removing the default commands.")
    scopes = [
    BotCommandScopeDefault(),
    BotCommandScopeAllPrivateChats(),
    BotCommandScopeAllGroupChats(),
    ]
    for scope in scopes:
        await bot.delete_my_commands(scope=scope)
        logger.info(f"Default commands removed from {scope}.")