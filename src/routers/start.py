from aiogram import Router 
from aiogram.filters import CommandStart 
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from messages import messages
from states import UserForm
from database.operations import set_user, get_user

start_router = Router()


@start_router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext) -> None:
    if not message.from_user: return
    user = await get_user(tg_id=message.from_user.id)
    if user:
        await message.answer("You are already registered")
        return

    await state.set_state(UserForm.name)
    await message.answer("\n".join(messages["start"]))


@start_router.message(UserForm.name)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(UserForm.education)
    await message.answer("\n".join(messages["education"]))


@start_router.message(UserForm.education)
async def process_education(message: Message, state: FSMContext) -> None:
    await state.update_data(education=message.text)
    data = await state.get_data()
    if message.from_user:
        await set_user(
            tg_id=message.from_user.id,
            username=data["name"],
            education=data["education"]
        )
    await state.clear()

