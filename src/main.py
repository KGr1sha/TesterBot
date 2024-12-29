import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher 
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from messages import messages
from forms import UserForm
from gigachat import use
from bot_settings import BotSettings

settings = BotSettings()

dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: Message, state: FSMContext) -> None:
    if message.from_user:
        settings.users[message.from_user.full_name] = {
            "model": "",
            "education": "",
        }
    await state.set_state(UserForm.education)
    await message.answer(messages["start"])


@dp.message(UserForm.education)
async def process_education(message: Message, state: FSMContext) -> None:
    await state.update_data(education=message.text)
    await state.set_state(UserForm.model)
    await message.answer(messages["model"])


@dp.message(UserForm.model)
async def process_mode(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("good")


@dp.message()
async def echo_handler(message: Message) -> None:
    if not message.text: return
    
    response = use(
        access_token=settings.gigachat_token,
        model="GigaChat",
        message_history=settings.message_history,
        proompt=message.text
    )

    await message.answer(response)



async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=settings.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
