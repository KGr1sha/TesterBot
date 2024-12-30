from aiogram import Router 
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.scene import Scene, on

from gigachat import use, get_access_token

class ChatScene(Scene, state="chat"):
    history = []
    access_token = ""

    @on.message.enter()
    async def on_enter(self, message: Message) -> None:
        await message.answer("gigachating")
        self.access_token = await get_access_token()

    @on.message()
    async def handle_message(self, message: Message) -> None:
        if not message.text: return

        response = await use(
            access_token=self.access_token,
            model="GigaChat",
            message_history=self.history,
            proompt=message.text
        )

        await message.answer(response)

chat_router = Router()
chat_router.message.register(ChatScene.as_handler(), Command("quiz"))
