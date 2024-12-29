import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher 
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from messages import messages
from forms import UserForm
from gigachat import use
from bot_settings import BotSettings

settings = BotSettings()

dp = Dispatcher()

async def send_messages(message: Message, messages: list) -> None:
    for m in messages:
        await message.answer(m)


@dp.message(CommandStart())
async def start_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(UserForm.name)
    await send_messages(message, messages["start"])


@dp.message(UserForm.name)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(UserForm.education)
    await send_messages(message, messages["education"])


@dp.message(UserForm.education)
async def process_education(message: Message, state: FSMContext) -> None:
    await state.update_data(education=message.text)
    data = await state.get_data()
    if message.from_user:
        id = message.from_user.full_name
        settings.users[id] = {
            "name": data["name"],
            "education": data["education"],
        }
        settings.message_history[id] = []
    await state.clear()


@dp.message(Command("users"))
async def list_users(message: Message) -> None:
    await message.answer(str(settings.users))



@dp.message(Command("history"))
async def show_history(message: Message) -> None:
    if message.from_user:
        id = message.from_user.full_name
        await message.answer(
            str(settings.message_history[id])
        )


@dp.message()
async def gigachat_handler(message: Message) -> None:
    if not message.text: return

    history = []
    if message.from_user:
        history = settings.message_history[message.from_user.full_name]

    response = use(
        access_token=settings.gigachat_token,
        model="GigaChat",
        message_history=history,
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
