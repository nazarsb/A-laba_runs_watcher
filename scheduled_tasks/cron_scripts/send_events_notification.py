import logging
import asyncio

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from database.enums.enums import UserRole
from bot.db_requests.db_requests import get_events, get_users_exept_role
from bot.config.config import Config, load_config

logger = logging.getLogger(__name__)

async def send_events_notification(bot: Bot, session_factory: async_sessionmaker) -> None:
    async with session_factory() as session:
        events = await get_events(session)
        users = await get_users_exept_role(session, UserRole.UNKNOWN)
        message_no_text = '<b>В А-лабе всё спокойно.\nЗапланированных событий нет. 😴</b>'
        message_text = '<b>☝🏼 В А-лабе есть грядущие события. \nЖми команду <u>/show_events</u> чтоб получить подробности</b>\n'

        for user in users:
            if events:
                message = message_text
            else:
                message = message_no_text
            await bot.send_message(chat_id=user, text=message)

async def main() -> None:
    config: Config = load_config()
    bot_kwargs = {
        "token": config.bot.token,
        "default": DefaultBotProperties(parse_mode=ParseMode.HTML),
    }
    if config.bot.proxy_url:
        bot_kwargs["session"] = AiohttpSession(proxy=config.bot.proxy_url)

    bot = Bot(**bot_kwargs)
    engine = create_async_engine(
        url=str('postgresql+psycopg://'+config.db.pg_user+':'+config.db.pg_password+'@' \
                +config.db.pg_host+':'+str(config.db.pg_port)+'/'+config.db.pg_db_name) \
                + "?options=-c%20timezone=Europe/Moscow")
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    try:
        await send_events_notification(bot, sessionmaker)
    finally:
        await bot.session.close()
        await engine.dispose()

try:
    asyncio.run(main())
except Exception as e:
    logger.exception(e)
