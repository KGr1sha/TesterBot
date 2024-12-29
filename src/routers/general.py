from aiogram import Router 
from aiogram.filters import Command
from aiogram.types import Message

general_router = Router()


@general_router.message(Command("users"))
async def list_users(message: Message) -> None:
    #await message.answer(str(settings.users))
    pass


@general_router.message(Command("history"))
async def show_history(message: Message) -> None:
    if message.from_user:
        id = message.from_user.full_name
        await message.answer(
            #str(settings.message_history[id])
            "hello"
        )

