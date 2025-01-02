from time import time

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery
)
from aiogram.fsm.scene import Scene, on
from aiogram.fsm.context import FSMContext

from llm import Gigachat
from states import TestCreation, Substate, TestingState
from database.operations import add_test, delete_test, get_test 
from database.models import TestStruct
from proomptgen import ProomptGenerator

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
        chat = Gigachat()
        await chat.init_token()
        generator = ProomptGenerator()

        proompt = generator.create_test(t)
        start = time()
        test = await chat.use(
            model="GigaChat",
            history=[],
            proompt=proompt
        )
        end = time()
        await message.answer(f"test generated. took {end - start} seconds")
        await message.answer(test)
        await message.answer(f"original proompt:\n{proompt}")

        added = await add_test(message.from_user.id, t, test)
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

        chat = Gigachat()
        await chat.init_token()
        generator = ProomptGenerator()

        if query.from_user.id not in message_history.keys():
            message_history[query.from_user.id] = list()

        proompt = generator.take_test(test.content_text)
        start = time()
        response = await chat.use(
            model="GigaChat",
            history=message_history[query.from_user.id],
            proompt=proompt
        )
        end = time()

        await query.message.edit_text(
            response + f"\n\ntook {end - start} seconds"
        )
        await state.update_data(substate=TestingState.taking_test)


    @on.message(Substate("substate", TestingState.taking_test))
    async def handle_take_state(self, message: Message, state: FSMContext) -> None:
        if not message.from_user or not message.text: return

        chat = Gigachat()
        await chat.init_token()

        response = await chat.use(
            model="GigaChat",
            history=message_history[message.from_user.id],
            proompt=message.text
        )
        await message.answer(response)


class DeletingTestScene(Scene, state="deleting_test"):
    @on.callback_query.enter()
    async def on_enter(self, query: CallbackQuery, state: FSMContext) -> None:
        if not query.data or not query.from_user: return
        test_id = int(query.data)
        await delete_test(test_id)
        await query.message.edit_text("test deleted")


test_router.message.register(CreateTestScene.as_handler(), Command("create_test"))
test_router.callback_query.register(TestingScene.as_handler(), TestingState.selecting_take)
test_router.callback_query.register(DeletingTestScene.as_handler(), TestingState.selecting_delete)

