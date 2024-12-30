from aiogram import Router 
from aiogram.filters import CommandStart 
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from messages import messages
from states import UserForm
from bot_settings import settings

start_router = Router()
users = {}

async def send_messages(message: Message, messages: list) -> None:
    for m in messages:
        await message.answer(m)


@start_router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(UserForm.name)
    await send_messages(message, messages["start"])


@start_router.message(UserForm.name)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(UserForm.education)
    await send_messages(message, messages["education"])


@start_router.message(UserForm.education)
async def process_education(message: Message, state: FSMContext) -> None:
    await state.update_data(education=message.text)
    data = await state.get_data()
    if message.from_user:
        id = message.from_user.full_name
        settings.users[id] = {
            "name": data["name"],
            "education": data["education"],
        }
    await state.clear()

