from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


class UserForm(StatesGroup):
    name = State()
    education = State()


class TestingState(StatesGroup):
    selecting_delete = State()
    selecting_take = State()


class TestCreation(StatesGroup):
    subject = State()
    theme = State()
    noq = State()
    qtype = State()
    difficulty = State()
    time = State()
    name = State()


class Substate(Filter):
    def __init__(self, substate_key: str, substate: State) -> None:
        self.substate = substate
        self.substate_key = substate_key

    async def __call__(self, message: Message, state: FSMContext) -> bool:
        return (await state.get_value(self.substate_key)) == self.substate

