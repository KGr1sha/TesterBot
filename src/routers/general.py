from aiogram import Router 
from aiogram.filters import Command
from aiogram.types import Message

from database.operations import delete_all_users, get_users, get_tests

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


@general_router.message(Command("tests"))
async def list_tests(message: Message) -> None:
    if not message.from_user: return

    id = message.from_user.id
    tests = await get_tests(id)
    if not tests:
        await message.answer("У вас  нету тестов")
    else:
        await message.answer(str(tests))


