from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button

from bot.dialogs.start_dialog.getters import getter_user
from bot.dialogs.start_dialog.states import StartSG   
from bot.dialogs.start_dialog.handlers import (click_new_run, click_new_event, click_alother_event)
from bot.dialogs.widgets.i18n import I18nFormat



start_dialog = Dialog(
    Window(
        I18nFormat('start_message'),
        Button(text=I18nFormat('new_run'), id='new_run', on_click=click_new_run),
        Button(text=I18nFormat('electro_turn_off'), id='new_event', on_click=click_new_event),
        Button(I18nFormat('another_event'), id='else_event', on_click=click_alother_event),
        getter=getter_user,
        state=StartSG.start
    ),
)
