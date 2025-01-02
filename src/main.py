import asyncio
import logging
import sys

from aiogram.fsm.scene import SceneRegistry
from aiogram import Dispatcher 
from aiogram.types import  BotCommand

from routers.test import TestingScene
from setup import bot, dispatcher, set_commands
from database.setup import create_tables
from routers import (
    general_router,
    start_router,
    chat_router,
    test_router,
    ChatScene,
    CreateTestScene,
    StartScene
)

def register(dispatcher: Dispatcher) -> None:
    dispatcher.include_router(general_router)
    dispatcher.include_router(start_router)
    dispatcher.include_router(chat_router)
    dispatcher.include_router(test_router)

    scene_registry = SceneRegistry(dispatcher)
    scene_registry.add(StartScene)
    scene_registry.add(ChatScene, router=chat_router)
    scene_registry.add(CreateTestScene, router=test_router)
    scene_registry.add(TestingScene, router=test_router)


async def main() -> None:
    commands = [
        BotCommand(command="start", description="Регистрация"),
        BotCommand(command="chat", description="Гигачат"),
        BotCommand(command="users", description="Список пользователей"),
        BotCommand(command="delusers", description="Удалить всех пользователей"),
        BotCommand(command="tests", description="Список тестов"),
        BotCommand(command="create_test", description="Создать тесе"),
    ]
    register(dispatcher)

    asyncio.gather(create_tables(), set_commands(commands))
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

