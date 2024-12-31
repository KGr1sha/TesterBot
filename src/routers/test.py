from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.scene import Scene, on
from aiogram.fsm.context import FSMContext

from gigachat import get_access_token, use 
from states import TestCreation, Substate

history = {}
access_token: str


class CreateTestScene(Scene, state="create_test"):
    @on.message.enter()
    async def on_enter(self, message: Message, state: FSMContext) -> None:
        await state.update_data(creation_state=TestCreation.subject)
        await message.answer("Создаем тест!")
        await message.answer("Предмет?")


    @on.message(Substate("creation_state", TestCreation.subject))
    async def handle_subject(self, message: Message, state: FSMContext) -> None:
        await state.update_data(subject=message.text)
        await state.update_data(creation_state=TestCreation.theme)
        await message.answer("Тема?")


    @on.message(Substate("creation_state", TestCreation.theme))
    async def handle_theme(self, message: Message, state: FSMContext) -> None:
        await state.update_data(theme=message.text)
        await state.update_data(creation_state=TestCreation.noq)
        await message.answer("Сколько вопросов?")


    @on.message(Substate("creation_state", TestCreation.noq))
    async def handle_noq(self, message: Message, state: FSMContext) -> None:
        await state.update_data(noq=message.text)
        await state.update_data(creation_state=TestCreation.difficulty)
        await message.answer("Сложность?")


    @on.message(Substate("creation_state", TestCreation.difficulty))
    async def handle_difficultly(self, message: Message, state: FSMContext) -> None:
        await state.update_data(difficulty=message.text)
        await state.update_data(creation_state=TestCreation.time)
        await message.answer("Время на выполнение?")


    @on.message(Substate("creation_state", TestCreation.time))
    async def handle_time(self, message: Message, state: FSMContext) -> None:
        await state.update_data(time=message.text)
        data = await state.get_data()
        print(str(data))
        await state.clear()
        await message.answer("GOOD")


test_router = Router()
test_router.message.register(CreateTestScene.as_handler(), Command("test"))

