from aiogram_dialog import DialogManager

from sqlalchemy.ext.asyncio import AsyncSession

from bot.db_requests.db_requests import get_events


async def getter_events(dialog_manager: DialogManager, session: AsyncSession, **kwargs):
    events = await get_events(session)
    return {'events': events}
 

