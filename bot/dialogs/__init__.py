from aiogram import Router
from .new_run_dialog.dialogs import new_run_dialog
from .start_dialog.dialogs import start_dialog
from .electro_dialog.dialogs import electro_dialog

def get_dialogs() -> list[Router]:
     return [
             start_dialog,
             new_run_dialog,
             electro_dialog,
          ]