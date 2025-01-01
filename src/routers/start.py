from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.scene import Scene, on
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from messages import messages
from states import Substate, UserForm
from database.operations import set_user, get_user

start_router = Router()

class StartScene(Scene, state="start"):
    @on.message.enter()
    async def start_handler(self, message: Message, state: FSMContext) -> None:
        print("ENTER START SCENE")
        if not message.from_user: return
        user = await get_user(tg_id=message.from_user.id)
        if user:
            await message.answer("You are already registered")
            await self.wizard.back()
            return

        await state.update_data(step=UserForm.name)
        await message.answer("\n".join(messages["start"]))

    @on.message(Substate("step", UserForm.name))
    async def process_name(self, message: Message, state: FSMContext) -> None:
        await state.update_data(name=message.text)
        await state.update_data(step=UserForm.education)
        await message.answer("\n".join(messages["education"]))

    @on.message(Substate("step", UserForm.education))
    async def process_education(self, message: Message, state: FSMContext) -> None:
        await state.update_data(education=message.text)
        data = await state.get_data()
        if message.from_user:
            await set_user(
                tg_id=message.from_user.id,
                username=data["name"],
                education=data["education"]
            )
        await message.answer(
            "Отлично! Можем переходить к генерации тестов!\nПопробуйте /create_test для создания нового теста"
        )
        await self.wizard.back()

start_router.message.register(StartScene.as_handler(), CommandStart())

