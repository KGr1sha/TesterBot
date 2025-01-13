from os import getenv
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher 
from aiogram.client.default import DefaultBotProperties
from aiogram.types import  BotCommandScopeAllPrivateChats, BotCommandScopeDefault,  BotCommand
from aiogram.fsm.storage.memory import SimpleEventIsolation

from llm import Gemini, Gigachat, ChatGPT

def get_bot_token() -> str:
    load_dotenv()
    bt = getenv("BOT_TOKEN")
    if not bt:
        raise Exception("Failed to get bot token from env")
    return bt

bot_token = get_bot_token()
bot = Bot(token=bot_token, default=DefaultBotProperties())
dispatcher = Dispatcher(
    events_isolation=SimpleEventIsolation(),
)
llm_client = Gemini()

async def set_commands(commands: list[BotCommand]) -> None:
    await bot.set_my_commands(commands, BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands, BotCommandScopeDefault())
