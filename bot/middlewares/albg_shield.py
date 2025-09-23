import logging
from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware, Bot
from aiogram.types import TelegramObject, User

logger = logging.getLogger(__name__)

class AlbgShieldMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        user: User = data.get('event_from_user') # type: ignore
        bot: Bot = data.get('bot') # type: ignore
        if user is not None:
            if user.id not in data['albg_users']:
                logger.warning('User %s not in albg_users list', user.id)
                await bot.send_message(chat_id=user.id, text='Доступ запрещён') # type: ignore
                await bot.send_message(chat_id=data['admins'][0], text=f'Пользователь [{user.id}] {user.first_name} пытался ворваться в чат.')
                return
        return await handler(event, data)