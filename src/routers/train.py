from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.fsm.scene import Scene, on
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from states import Substate, TrainingState 
from database.models import TrainingData
from proomptgen import ProomptGenerator
from setup import llm_client
from keyboards import difficulty_keyboard, question_type_keyboard, train_keyboard

train_router = Router()

message_history = {}


class TrainingScene(Scene, state="training"):
    @on.message.enter()
    async def on_enter(self, message: Message, state: FSMContext) -> None:
        await message.answer("Режим тренировки!")
        await message.answer("Предмет?")
        await state.update_data(trainstate=TrainingState.subject)


    @on.message(Substate("trainstate", TrainingState.subject))
    async def handle_subject(self, message: Message, state: FSMContext) -> None:
        await state.update_data(subject=message.text)
        await state.update_data(trainstate=TrainingState.theme)
        await message.answer("Тема?")


    @on.message(Substate("trainstate", TrainingState.theme))
    async def handle_theme(self, message: Message, state: FSMContext) -> None:
        await state.update_data(theme=message.text)
        await state.update_data(trainstate=TrainingState.question_type)
        await message.answer("Тип вопросов", reply_markup=question_type_keyboard())


    @on.message(Substate("trainstate", TrainingState.question_type))
    async def handle_qtype(self, message: Message, state: FSMContext) -> None:
        await state.update_data(qtype=message.text)
        await state.update_data(trainstate=TrainingState.difficulty)
        await message.answer("Сложность?", reply_markup=difficulty_keyboard())


    @on.message(Substate("trainstate", TrainingState.difficulty))
    async def handle_difficultly(self, message: Message, state: FSMContext) -> None:
        if not message.from_user: return

        await state.update_data(difficulty=message.text)
        await state.update_data(trainstate=TrainingState.training)
        data = await state.get_data()
        t = TrainingData(
            subject=data["subject"],
            theme=data["theme"],
            question_type=data["qtype"],
            difficulty=data["difficulty"],
        )

        generator = ProomptGenerator()
        id = message.from_user.id
        message_history[id] = list()
        response = await llm_client.use(
            history=message_history[id],
            proompt=generator.train(t)
        )

        await message.answer(response, reply_markup=train_keyboard())


    @on.message(Substate("trainstate", TrainingState.training))
    async def handle_take_state(self, message: Message) -> None:
        if not message.from_user or not message.text: return

        id = message.from_user.id 
        response = await llm_client.use(
            history=message_history[id],
            proompt=message.text
        )
        await message.answer(response, reply_markup=train_keyboard())


    @on.message(F.text == "Закончить тренировку")
    async def exit(self, _: Message) -> None:
        await self.wizard.exit()

    
    @on.message.exit()
    async def on_exit(self, message: Message) -> None:
        await message.answer(
            "Тренировка закончена",
            reply_markup=ReplyKeyboardRemove()
        )


train_router.message.register(TrainingScene.as_handler(), Command("train"))

