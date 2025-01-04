from time import time

from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery
)
from aiogram.fsm.scene import Scene, on
from aiogram.fsm.context import FSMContext

from states import TestCreation, Substate, TestingState
from database.operations import add_test, delete_test, get_test, get_user
from database.models import TestData
from proomptgen import ProomptGenerator
from setup import llm_client

test_router = Router()

message_history = {}


class CreateTestScene(Scene, state="create_test"):
    @on.message.enter()
    async def on_enter(self, message: Message, state: FSMContext) -> None:
        if not message.from_user: return
        user = await get_user(message.from_user.id)
        if not user:
            await message.answer("Вы не зарегестрированы. Напишите /start")
            return
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
        t = TestData(
            data["subject"],
            data["theme"],
            data["noq"],
            data["qtype"],
            data["difficulty"],
            data["time"],
        )
        await message.answer("генерация теста...")
        generator = ProomptGenerator()

        proompt = generator.create_test(t)
        test = await llm_client.use(proompt)

        added = await add_test(message.from_user.id, t, test)
        if not added:
            await message.answer("Ошибка при добавлении теста")
            return;

        await message.answer("Тест добавлен!\nЧтобы пройти его используйте /take_test")
        await state.clear()


class TestingScene(Scene, state="testing"):
    @on.callback_query.enter()
    async def on_enter(self, query: CallbackQuery, state: FSMContext) -> None:
        if not query.data or not query.from_user: return
        test_id = int(query.data)
        test = await get_test(test_id)
        if not test:
            query.answer("Ошибка")
            return

        generator = ProomptGenerator()

        message_history[query.from_user.id] = list()

        proompt = generator.take_test(test.content_text)
        response = await llm_client.use(
            history=message_history[query.from_user.id],
            proompt=proompt
        )

        await query.message.edit_text(response)
        await state.update_data(substate=TestingState.taking_test)


    @on.message(Substate("substate", TestingState.taking_test))
    async def handle_take_state(self, message: Message) -> None:
        if not message.from_user or not message.text: return

        response = await llm_client.use(
            history=message_history[message.from_user.id],
            proompt=message.text
        )
        await message.answer(response)


class DeletingTestScene(Scene, state="deleting_test"):
    @on.callback_query.enter()
    async def on_enter(self, query: CallbackQuery) -> None:
        if not query.data or not query.from_user: return
        test_id = int(query.data)
        await delete_test(test_id)
        await query.message.edit_text("Тест удален")


test_router.message.register(CreateTestScene.as_handler(), Command("create_test"))
test_router.callback_query.register(TestingScene.as_handler(), TestingState.selecting_take)
test_router.callback_query.register(DeletingTestScene.as_handler(), TestingState.selecting_delete)

