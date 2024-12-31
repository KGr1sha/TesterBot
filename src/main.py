import asyncio
import logging
import sys
from aiogram.fsm.scene import SceneRegistry
from dotenv import load_dotenv
from os import getenv

from aiogram import Bot, Dispatcher 
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommandScopeDefault,  BotCommand
from aiogram.fsm.storage.memory import SimpleEventIsolation

from routers import (
    start_router,
    general_router,
    chat_router,
    test_router,
    ChatScene,
    CreateTestScene,
)
from database.setup import create_tables


def create_dispatcher() -> Dispatcher:
    dispatcher = Dispatcher(
        events_isolation=SimpleEventIsolation()
    )
    dispatcher.include_router(start_router)
    dispatcher.include_router(chat_router)
    dispatcher.include_router(general_router)
    dispatcher.include_router(test_router)

    scene_registry = SceneRegistry(dispatcher)
    scene_registry.add(ChatScene)
    scene_registry.add(CreateTestScene)
    return dispatcher


async def set_commands(bot: Bot) -> None:
    commands = [
        BotCommand(command="start", description="Старт"),
        BotCommand(command="users", description="Список пользователей"),
        BotCommand(command="chat", description="Гигачат"),
        BotCommand(command="delusers", description="Удалить всех пользователей"),
        BotCommand(command="create_test", description="Тест?"),
        BotCommand(command="tests", description="Список тестов"),
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


def get_bot_token() -> str:
    load_dotenv()
    bt = getenv("BOT_TOKEN")
    if not bt:
        raise Exception("Failed to get bot token from env")
    return bt


async def main() -> None:
    dp = create_dispatcher()
    bot_token = get_bot_token()

    bot = Bot(token=bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    asyncio.gather(create_tables(), set_commands(bot))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

