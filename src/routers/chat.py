from aiogram import Router 
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.scene import Scene, on

from gigachat import get_access_token, use 

history = []
access_token: str

class ChatScene(Scene, state="chat"):

    @on.message.enter()
    async def on_enter(self, message: Message) -> None:
        global access_token
        access_token = await get_access_token()
        await message.answer("gigachating")


    @on.message()
    async def handle_message(self, message: Message) -> None:
        if not message.text: return

        response = await use(
            access_token=access_token,
            model="GigaChat",
            message_history=history,
            proompt=message.text
        )

        await message.answer(response)

chat_router = Router()
chat_router.message.register(ChatScene.as_handler(), Command("chat"))
