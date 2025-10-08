from typing import Callable, Awaitable, Dict, Any, cast

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from cachetools import TTLCache
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db_requests.db_requests import upsert_user, get_users_id
from database.enums.enums import UserRole
from pprint import pprint

class TrackAllUsersMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        
        session: AsyncSession = data.get("session")
        user = data.get("event_from_user")

        await upsert_user(
            session=session,
            telegram_id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            user_role=UserRole.UNKNOWN
        )

        return await handler(event, data)