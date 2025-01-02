from time import time

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import (Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
    CallbackQuery
)
from aiogram.fsm.scene import Scene, on
from aiogram.fsm.context import FSMContext

from gigachat import get_access_token, use
from states import TestCreation, Substate
from database.operations import add_test, get_test
from database.models import TestStruct
from testgen import ProomptGenerator
from proompts import get_proompt

test_router = Router()

access_token: str
message_history = {}


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
        await state.update_data(creation_state=TestCreation.qtype)
        await message.answer("Тип вопросов?")


    @on.message(Substate("creation_state", TestCreation.qtype))
    async def handle_qtype(self, message: Message, state: FSMContext) -> None:
        await state.update_data(qtype=message.text)
        await state.update_data(creation_state=TestCreation.difficulty)
        await message.answer("Сложность?")


    @on.message(Substate("creation_state", TestCreation.difficulty))
    async def handle_difficultly(self, message: Message, state: FSMContext) -> None:
        await state.update_data(difficulty=message.text)
        await state.update_data(creation_state=TestCreation.time)
        await message.answer("Время на выполнение?")


    @on.message(Substate("creation_state", TestCreation.time))
    async def handle_time(self, message: Message, state: FSMContext) -> None:
        if not message.from_user: return

        await state.update_data(time=message.text)
        data = await state.get_data()
        t = TestStruct(
            data["subject"],
            data["theme"],
            data["noq"],
            data["qtype"],
            data["difficulty"],
            data["time"],
        )
        await message.answer("генерация теста...")
        gigatoken = await get_access_token()
        generator = ProomptGenerator(gigatoken)
        start = time()
        test = await generator.generate_test(t)
        end = time()
        await message.answer(f"test generated. took {end - start} seconds")
        await message.answer(test[0])
        await message.answer(f"original proompt:\n{test[1]}")

        added = await add_test(message.from_user.id, t, test[0])
        if added:
            await message.answer("test added")
        else:
            await message.answer("user not present")

        await state.clear()


class TestingScene(Scene, state="testing"):
    @on.callback_query.enter()
    async def on_enter(self, query: CallbackQuery, state: FSMContext) -> None:
        if not query.data or not query.from_user: return
        test_id = int(query.data)
        test = await get_test(test_id)
        if not test:
            query.answer("error")
            return


        generator = ProomptGenerator(await get_access_token())
        start = time()
        result = await generator.take_test(test.content_text)
        end = time()

        await query.message.edit_text(
            result[0] + f"\n\ntook {end - start} seconds\n\n"\
            + f"original prooompt:\n{result[1]}"
        )





test_router.message.register(CreateTestScene.as_handler(), Command("create_test"))
test_router.callback_query.register(TestingScene.as_handler())

