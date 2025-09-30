import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeAllPrivateChats, BotCommandScopeAllGroupChats, BotCommandScopeChatMember, BotCommandScopeChat
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from aiogram.fsm.storage.base import DefaultKeyBuilder

from aiogram_dialog import setup_dialogs

from redis.asyncio.client import Redis
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from bot.config.config import Config, load_config
from bot.handlers import get_routers
from bot.dialogs import get_dialogs
from bot.middlewares import albg_shield, logging_middleware, session, track_all_users
from bot.dialogs.new_run_dialog.dialogs import new_run_dialog
from bot.dialogs.start_dialog.dialogs import start_dialog
from bot.keyboards.menu_buttons import get_main_menu_commands, menu_set_up, menu_drop_down

from pprint import pprint

logger = logging.getLogger(__name__)

async def main() -> None:
    logger.info('Starting bot')

    logger.info('loading congig')
    config: Config = load_config()

    logger.info('Setting up redis')
    redis = Redis(host=config.redis.host, 
                  port=config.redis.port) # стучится в контейнер redis_test
    storage = RedisStorage(redis=redis, 
                           key_builder=DefaultKeyBuilder(with_destiny=True))

    bot = Bot(token=config.bot.token,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=storage)

    logger.info('Setting up sqlalchemy')
    engine = create_async_engine(
        url=str('postgresql+psycopg://'+config.db.pg_user+':'+config.db.pg_password+'@' \
                +config.db.pg_host+':'+str(config.db.pg_port)+'/'+config.db.pg_db_name) \
                + "?options=-c%20timezone=Europe/Moscow")
    Sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    logger.info("Including routers and dialogs")
    dp.include_routers(*get_routers(), *get_dialogs())

    logger.info("Setting up dialogs")
    # bg_factory = setup_dialogs(dp)
    setup_dialogs(dp)    

    dp.update.outer_middleware(session.DbSessionMiddleware(Sessionmaker))
    dp.update.middleware(logging_middleware.LoggingMiddleware())
    dp.update.outer_middleware(track_all_users.TrackAllUsersMiddleware())
    dp.update.outer_middleware(albg_shield.AlbgShieldMiddleware())

    dp.startup.register(menu_set_up)
    dp.shutdown.register(menu_drop_down)

    # try:
        # await asyncio.gather(
        #     dp.start_polling(
        #         bot,
        #         bg_factory=bg_factory,
        #     )
        # )
    #     await asyncio.gather(
    #     setup_dialogs(dp),
    #     dp.start_polling(bot))
    # except Exception as e:
    #     logger.exception(e)
    # finally:
    #     await bot.session.close()
    #     logger.info("Connection to Postgres closed")
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except Exception as e:
        logger.exception(e)
    finally:
        await bot.session.close()
        logger.info("Connection to Postgres closed")

