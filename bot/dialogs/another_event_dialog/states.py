from aiogram.fsm.state import State, StatesGroup

class AnotherEventSG(StatesGroup):
    another_event = State()
    event_name = State()
    event_start_date = State()
    event_end_date = State()
    event_start_time = State()
    event_end_time = State()
    summary = State()