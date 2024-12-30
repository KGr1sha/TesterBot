from aiogram.fsm.state import State, StatesGroup

class UserForm(StatesGroup):
    name = State()
    education = State()


class BotState(StatesGroup):
    registration = State()
    test = State()
    exam = State()
    idle = State()
