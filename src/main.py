import asyncio
import logging
import sys

from aiogram.fsm.scene import SceneRegistry
from aiogram import Dispatcher 
from aiogram.types import BotCommand, BotCommandScopeAllChatAdministrators, BotCommandScopeAllGroupChats, BotCommandScopeAllPrivateChats, BotCommandScopeChat, BotCommandScopeDefault 

from routers.test import DeletingTestScene, TestingScene
from setup import bot, dispatcher, set_commands, llm_client
from database.setup import create_tables
from routers import (
    general_router,
    start_router,
    chat_router,
    test_router,
    train_router,
    ChatScene,
    CreateTestScene,
    StartScene,
    TrainingScene
)

def register(dispatcher: Dispatcher) -> None:
    dispatcher.include_router(general_router)
    dispatcher.include_router(start_router)
    dispatcher.include_router(chat_router)
    dispatcher.include_router(test_router)
    dispatcher.include_router(train_router)

    scene_registry = SceneRegistry(dispatcher)
    scene_registry.add(StartScene, router=start_router)
    scene_registry.add(ChatScene, router=chat_router)
    scene_registry.add(CreateTestScene, router=test_router)
    scene_registry.add(TestingScene, router=test_router)
    scene_registry.add(DeletingTestScene, router=test_router)
    scene_registry.add(TrainingScene, router=train_router)



async def on_startup():
    commands = [
        BotCommand(command="start", description="Регистрация"),
        BotCommand(command="chat", description="Гигачат"),
        BotCommand(command="users", description="Список пользователей"),
        BotCommand(command="take_test", description="Пройти тест"),
        BotCommand(command="delete_test", description="Удалить тест"),
        BotCommand(command="create_test", description="Создать тест"),
        BotCommand(command="train", description="Режим тренировки"),
    ]
    #await bot.set_my_commands([], BotCommandScopeAllPrivateChats())

    register(dispatcher)
    asyncio.gather(
        create_tables(),
        llm_client.init_token(),
        set_commands(commands)
    )


async def main() -> None:
    dispatcher.startup.register(on_startup)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

