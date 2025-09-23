import asyncio
import logging

from bot.bot import main
from bot.config.config import Config, load_config

if __name__ == '__main__':
    config: Config = load_config()

    logging.basicConfig(
    level=logging.getLevelName(config.logs.level), format=config.logs.format
)

    asyncio.run(main())
    