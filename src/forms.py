from aiogram.fsm.state import State, StatesGroup

class UserForm(StatesGroup):
    education = State()
    model = State()
