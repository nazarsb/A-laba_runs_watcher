from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button

from bot.dialogs.start_dialog.getters import getter_user
from bot.dialogs.start_dialog.states import StartSG   
from bot.dialogs.start_dialog.handlers import (click_new_run, click_new_event, click_alother_event)



start_dialog = Dialog(
    Window(
        Format('Привет, {name}!\n\n'
               'Запланировать новое событие?\n'
               'Еще можешь выбирать команды в меню внизу слева.', when='is_first'),
        Const('📝 Какое событие запланировать?'),
        Button(text=Const('🚀 Новый запуск'), id='new_run', on_click=click_new_run),
        Button(text=Const('⚠️ Отключение энергии'), id='new_event', on_click=click_new_event),
        Button(Const('Другое'), id='else_event', on_click=click_alother_event),
        getter=getter_user,
        state=StartSG.start
    ),
)
