import logging
from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware, Bot
from aiogram.types import TelegramObject, User
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db_requests.db_requests import get_users_id, get_users_by_role, get_super_admin_id
from database.enums.enums import UserRole

from pprint import pprint

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
        session: AsyncSession = data.get('session') # type: ignore
        users_id = await get_users_id(session=session)
        restricted_users = await get_users_by_role(session=session, role=UserRole.UNKNOWN)
        super_admin = await get_super_admin_id(session=session)
        if user is not None:
            if user.id not in users_id or user.id in restricted_users:
                logger.warning('User %s not in allowed users list', user.id)
                await bot.send_message(chat_id=user.id, text='Доступ запрещён') # type: ignore
                await bot.send_message(chat_id=super_admin, text=f'Пользователь [{user.id}] {user.first_name} пытался ворваться в чат.')
                return
        return await handler(event, data)