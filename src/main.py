import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message

from gigachat import use, get_access_token
from bot_settings import settings, init_settings
from routers import start_router, general_router


dp = Dispatcher()
dp.include_router(start_router)
dp.include_router(general_router)


#@dp.message()
#async def gigachat_handler(message: Message, state: FSMContext) -> None:
#    if not message.text: return
#    if message.from_user:
#        id = message.from_user.full_name
#        if id not in settings.users:
#            raise Exception(f"USER NOT REGISTERED: {id}")
#            #await start_handler(message, state)
#
#    history = []
#    if message.from_user:
#        history = settings.message_history[message.from_user.full_name]
#
#    response = use(
#        access_token=settings.gigachat_token,
#        model=settings.model,
#        message_history=history,
#        proompt=message.text
#    )
#
#    await message.answer(response)


async def main() -> None:
    gigatoken = await get_access_token()
    init_settings(gigatoken, "GigaChat")
    bot = Bot(token=settings.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

