import logging
from aiogram import BaseMiddleware
from aiogram.types import Update

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseMiddleware):
  async def __call__(
      self, 
      handler, 
      event: Update, 
      data: dict
      ):
    userm = event.message
    userc = event.callback_query
   # logger.info(f"RAW UPD: {event}")
    if event.message:
      logger.info("Update_message: tg_id=%s, username=%s, flulname=%s >> %s", 
                  userm.from_user.id, 
                  userm.from_user.username,
                  userm.from_user.full_name,
                  event.message.text
                  )
    elif event.callback_query:
      logger.info("Update_message: tg_id=%s, username=%s, flulname=%s >> %s", 
                  userc.from_user.id, 
                  userc.from_user.username,
                  userc.from_user.full_name,
                  event.callback_query.data
                  )
    return await handler(event, data)