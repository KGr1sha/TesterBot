from aiogram import Router 
from aiogram.types import Message 
from aiogram.enums import ParseMode

from setup import llm_client
max_history_size = 30
history = {}
fallback_router = Router()

@fallback_router.message()
async def handle_random_message(message: Message):
    if not message.text or not message.from_user: return
    user_id = message.from_user.id
    if user_id not in history.keys():
        history[user_id] = list()

    response = await llm_client.use(
        history=history[message.from_user.id],
        proompt=message.text + "\nОтвечай на русском"
    )

    await message.answer(response, parse_mode=ParseMode.MARKDOWN)
