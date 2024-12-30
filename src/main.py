import asyncio
import logging
import sys
from dotenv import load_dotenv
from os import getenv

from aiogram import Bot, Dispatcher 
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommandScopeDefault,  BotCommand

from routers import start_router, general_router
from database.setup import create_tables


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

async def set_commands(bot: Bot) -> None:
    commands = [
        BotCommand(command="start", description="Старт"),
        BotCommand(command="users", description="Список пользователей"),
        BotCommand(command="history", description="История сообщений"),
        BotCommand(command="delusers", description="Удалить всех пользователей"),
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())

def get_bot_token() -> str:
    load_dotenv()
    bt = getenv("BOT_TOKEN")
    if not bt:
        raise Exception("Failed to get bot token from env")
    return bt

async def main() -> None:
    bot_token = get_bot_token()
    bot = Bot(token=bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    asyncio.gather(create_tables(), set_commands(bot))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

