from aiogram.fsm.state import State, StatesGroup

class RunSG(StatesGroup):
    new_run = State()
    run_date = State()
    reagent_kit = State()
    summary = State()
    edit = State()
