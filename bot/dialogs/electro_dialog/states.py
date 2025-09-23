from aiogram.fsm.state import State, StatesGroup

class ElectroSG(StatesGroup):
    event_start_date = State()
    event_end_date = State()
    event_time = State()
    event_start_time = State()
    event_end_time = State()
    summary = State()
