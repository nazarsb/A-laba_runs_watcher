import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from fluentogram import TranslatorHub
import pprint
logger = logging.getLogger(__name__)


class TranslatorRunnerMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:

        user: User = data.get('event_from_user')

        if user is None:
            return await handler(event, data)

        hub: TranslatorHub = data.get("translator_hub")
        print(hub)
        print(user.language_code)
        print(isinstance(hub, TranslatorHub))
        pprint.pprint(data)
        data['i18n'] = hub.get_translator_by_locale(locale=user.language_code)

        return await handler(event, data)