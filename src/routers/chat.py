from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.scene import Scene, on

from setup import llm_client

history = {}

class ChatScene(Scene, state="chat"):
    @on.message.enter()
    async def on_enter(self, message: Message) -> None:
        if message.from_user:
            history[message.from_user.id] = list()

        markup = ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text="Закончить чат")],
        ], resize_keyboard=True)
        await message.answer("Режим чата", reply_markup=markup)


    @on.message.exit()
    async def on_exit(self, message: Message) -> None:
        await message.answer("Чат закончился", reply_markup=ReplyKeyboardRemove())


    @on.message(F.text == "Закончить чат")
    async def exit(self, _: Message) -> None:
        await self.wizard.exit()


    @on.message(F.text)
    async def handle_message(self, message: Message) -> None:
        if not message.text or not message.from_user: return

        response = await llm_client.use(
            history=history[message.from_user.id],
            proompt=message.text
        )

        await message.answer(response, parse_mode=ParseMode.MARKDOWN)


chat_router = Router()
chat_router.message.register(ChatScene.as_handler(), Command("chat"))

