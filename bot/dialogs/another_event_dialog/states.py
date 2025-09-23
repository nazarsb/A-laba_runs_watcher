from aiogram.fsm.state import State, StatesGroup

class AnotherEventSG(StatesGroup):
    another_event = State()
    event_name = State()
    event_date = State()
    summary = State()
    edit = State()