from aiogram import Router
from .new_run_dialog.dialogs import new_run_dialog
from .start_dialog.dialogs import start_dialog
from .electro_dialog.dialogs import electro_dialog
from .show_events_dialog.dialogs import show_events_dialog
from .another_event_dialog.dialogs import another_event_dialog

def get_dialogs() -> list[Router]:
     return [
             start_dialog,
             new_run_dialog,
             electro_dialog,
             show_events_dialog,
             another_event_dialog
          ]