from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.scene import Scene, on

from gigachat import get_access_token, use 

history = {}
access_token: str

class ChatScene(Scene, state="chat"):
    @on.message.enter()
    async def on_enter(self, message: Message) -> None:
        global access_token
        access_token = await get_access_token()
        if message.from_user:
            history[message.from_user.id] = list()

        markup = ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text="exit")],
            [KeyboardButton(text="history")],
        ], resize_keyboard=True)
        await message.answer("gigachating", reply_markup=markup)


    @on.message.exit()
    async def on_exit(self, message: Message) -> None:
        await message.answer("chat ended", reply_markup=ReplyKeyboardRemove())


    @on.message(F.text == "exit")
    async def exit(self, message: Message) -> None:
        await self.wizard.exit()


    @on.message(F.text == "history")
    async def bomba(self, message: Message) -> None:
        if not message.from_user: return
        id = message.from_user.id
        if not history[id]:
            await message.answer("no messages with gigachat yet")
        await message.answer(str(history[id]))


    @on.message(F.text)
    async def handle_message(self, message: Message) -> None:
        if not message.text or not message.from_user: return

        response = await use(
            access_token=access_token,
            model="GigaChat",
            message_history=history[message.from_user.id],
            proompt=message.text
        )

        await message.answer(response, parse_mode=ParseMode.MARKDOWN)


chat_router = Router()
chat_router.message.register(ChatScene.as_handler(), Command("chat"))
