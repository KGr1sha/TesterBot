from aiogram import Router 
from aiogram.types import Message 

fallback_router = Router()

@fallback_router.message()
async def handle_random_message(message: Message):
    await message.answer("🙃 я не знаю таких комманд, я всего лишь бот.\nНапишите /help чтобы посмотреть всё, что я умею")
