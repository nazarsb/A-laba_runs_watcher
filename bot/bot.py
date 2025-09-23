import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from aiogram.fsm.storage.base import DefaultKeyBuilder

from aiogram_dialog import setup_dialogs

from redis.asyncio.client import Redis

from bot.config.config import Config, load_config
from bot.handlers import get_routers
from bot.dialogs import get_dialogs
from bot.middlewares import albg_shield, logging_middleware
from bot.dialogs.new_run_dialog.dialogs import new_run_dialog
from bot.dialogs.start_dialog.dialogs import start_dialog

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

    # engine = create_async_engine(
    #     url=str(config.db.dsn) + "?options=-c%20timezone=Europe/Moscow", echo=config.db.is_echo)
    # Sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    logger.info("Including routers and dialogs")
    dp.include_routers(*get_routers(), *get_dialogs())

    logger.info("Setting up dialogs")
    # bg_factory = setup_dialogs(dp)
    setup_dialogs(dp)

    dp.workflow_data.update({'albg_users': config.bot.albg_users,
                             'admins': config.bot.admins})
    
    dp.update.middleware(logging_middleware.LoggingMiddleware())
    dp.update.outer_middleware(albg_shield.AlbgShieldMiddleware())

    # dp.update.outer_middleware(session.DbSessionMiddleware(Sessionmaker))

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
    # finally:
    #     await bot.session.close()
    #     logger.info("Connection to Postgres closed")

