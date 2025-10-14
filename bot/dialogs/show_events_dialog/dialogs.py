from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.text import Format, List, Case, Multi

from bot.dialogs.show_events_dialog.getters import getter_events
from bot.dialogs.show_events_dialog.states import ShowEventsSG
from bot.dialogs.widgets.i18n import I18nFormat


def is_run_selector(data: dict, case: Case, dialog_manager: DialogManager):
    if data['item']['instrument']:
        if data['item']['instrument'] == 'Qnome-3841':
            return 'qnome'
        return 'run'
    if data['item']['event_name']:
        return 'another_event'
    else:
        return 'electro'

def is_there_event_selector(data: dict, case: Case, dialog_manager: DialogManager): 
    return 'events' in data and bool(data['events'])

show_events_dialog = Dialog(
    Window(
        Case(
            texts={
               True:  I18nFormat('planned_events'),
               False: I18nFormat('no_events_planned'),
            },
            selector=is_there_event_selector,
        ),
        List(
            field=Case(
                        texts={
                            'run': Multi(
                                    Format('<b>🚀 {item[event_type]}:</b> \
                                            <b>\n{item[date_start]} - {item[date_end]}</b> \
                                            \n{item[instrument]} на {item[reagent]}'),
                                    ),
                            'qnome': Multi(
                                    Format('<b>🚀 {item[event_type]}:</b> \
                                            <b>\n{item[date_start]} - {item[date_end]}</b> \
                                            \n{item[instrument]}'),
                                    ),
                            'electro': Multi(
                                    Format('<b>⚠️ {item[event_type]}:</b> \
                                            <b>\n{item[date_start]} - {item[date_end]}</b>')
                                    ),
                            'another_event': Multi(
                                    Format('<b>⚠️ {item[event_name]}:</b> \
                                            <b>\n{item[date_start]} - {item[date_end]}</b>')
                                    ),
                        },
                        selector=is_run_selector),
            items='events',
            sep='\n\n'
        ),
        getter=getter_events,
        state=ShowEventsSG.start        
    ),
)

