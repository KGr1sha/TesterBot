import asyncio
import logging
import sys
from dotenv import load_dotenv
from os import getenv

from aiogram import Bot, Dispatcher 
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommandScopeDefault,  BotCommand

from routers import start_router, general_router, chat_router, ChatScene
from database.setup import create_tables


dp = Dispatcher()
dp.include_router(start_router)
dp.include_router(general_router)

def create_dispatcher() -> Dispatcher:
    return Dispatcher()


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

