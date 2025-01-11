from os import getenv

from dotenv import load_dotenv
import asyncio

from aiogram import Bot, Dispatcher 
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import  BotCommandScopeAllPrivateChats, BotCommandScopeDefault,  BotCommand
from aiogram.fsm.storage.memory import SimpleEventIsolation

from llm import Gemini

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

async def set_commands(commands: list[BotCommand]) -> bool:
    return await bot.set_my_commands(commands, BotCommandScopeAllPrivateChats())
