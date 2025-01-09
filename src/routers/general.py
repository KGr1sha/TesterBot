from aiogram import Router 
from aiogram.filters import Command 
from aiogram.types import Message 
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext

from database.models import TestData
from database.operations import get_user, get_users, get_tests
from states import TestingState

general_router = Router()

async def list_tests(message: Message) -> None:
    if not message.from_user: return

    id = message.from_user.id
    tests = await get_tests(id)
    if not tests:
        await message.answer("У вас  нету тестов")
        return None

    builder = InlineKeyboardBuilder()
    for test in tests:
        settings: TestData = test["settings"]
        builder.button(
            text=f"{settings.subject} | {settings.theme} | {test["created_at"]} | {test["last_score"]}",
            callback_data=f"{test["id"]}",
        )
    builder.adjust(1, True)
    await message.answer("Тесты:", reply_markup=builder.as_markup())


@general_router.message(Command("users"))
async def list_users(message: Message) -> None:
    users = await get_users()
    if not users:
        await message.answer("Нет зарегестрированных пользователей")
        return None
    response = ""
    for user in users:
        response += str(user) + "\n"
    await message.answer(response)


@general_router.message(Command("stats"))
async def show_stats(message: Message) -> None:
    if not message.from_user: return

    user = await get_user(message.from_user.id)
    if not user:
        await message.answer("Ошибка. Проверьте, что вы зарагестрировались (/start)")
        return
    total = user["total_answers"]
    right = user["right_answers"]
    await message.answer(f"""Правильных ответов: {right}\nВсего ответов: {total}\nПроцент правильных ответов: {"{0:.2f}".format(float(right)/total * 100)}%""")


@general_router.message(Command("take_test"))
async def handle_tests(message: Message, state: FSMContext) -> None:
    await list_tests(message)
    await state.set_state(TestingState.selecting_take)


@general_router.message(Command("delete_test"))
async def handle_delete_tests(message: Message, state: FSMContext) -> None:
    await list_tests(message)
    await state.set_state(TestingState.selecting_delete)


@general_router.message(Command("help"))
async def show_help(message: Message):
    await message.answer("Помогаю бро")

