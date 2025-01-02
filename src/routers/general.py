from aiogram import Router 
from aiogram.filters import Command 
from aiogram.types import CallbackQuery, Message 
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext

from database.models import TestStruct
from database.operations import delete_all_users, get_test, get_users, get_tests
from states import TestingState

general_router = Router()


@general_router.message(Command("users"))
async def list_users(message: Message) -> None:
    users = await get_users()
    if not users:
        await message.answer("No registered users")
        return None
    response = ""
    for user in users:
        response += str(user) + "\n"
    await message.answer(response)


@general_router.message(Command("delusers"))
async def delusers_handler(message: Message) -> None:
    deleted = await delete_all_users()
    await message.answer(f"deleted {deleted} users")


@general_router.message(Command("take_test"))
async def handle_tests(message: Message, state: FSMContext) -> None:
    await list_tests(message)
    await state.set_state(TestingState.selecting_take)


@general_router.message(Command("delete_test"))
async def handle_delete_tests(message: Message, state: FSMContext) -> None:
    await list_tests(message)
    await state.set_state(TestingState.selecting_delete)


async def list_tests(message: Message) -> None:
    if not message.from_user: return

    id = message.from_user.id
    tests = await get_tests(id)
    if not tests:
        await message.answer("У вас  нету тестов")
        return None

    builder = InlineKeyboardBuilder()
    for test in tests:
        settings: TestStruct = test["settings"]
        builder.button(
            text=f"{settings.subject} | {settings.theme} | {test["created_at"]}",
            callback_data=f"{test["id"]}",
        )
    builder.adjust(1, True)
    await message.answer("Тесты:", reply_markup=builder.as_markup())


#@general_router.callback_query()
#async def handle_test_selection(query: CallbackQuery, state: FSMContext) -> None:
#    if not query.data: return
#    test_id = int(query.data)
#    test = await get_test(test_id)
#    if not test:
#        query.answer("error")
#        return
#
#    await query.message.edit_text(test.content_text)
#    
