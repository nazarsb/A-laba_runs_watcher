from aiogram import Router
from . import (
    user_handlers
               )

def get_routers() -> list[Router]:
     return [user_handlers.router,
          ]