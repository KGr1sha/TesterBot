from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup
from aiogram.fsm.scene import Scene, on
from aiogram.fsm.context import FSMContext

from states import Substate, TrainingState 
from database.models import TrainingData 
from database.operations import  update_user_activity
from proomptgen import ProomptGenerator
from setup import llm_client, bot
from keyboards import(
    difficulty_keyboard,
    question_type_keyboard,
    train_keyboard,
    truefalse_keyboard,
    answers_keyboard
)
from parser import parse_answers

train_router = Router()

message_history = {}

async def ask_question(user_id: int, question: str, question_type: str):
    markup: ReplyKeyboardMarkup|ReplyKeyboardRemove
    
    if question_type == "С выбором вариантов ответа":
        markup = answers_keyboard(parse_answers(question))
    elif question_type == "Верно/неверно":
        markup = truefalse_keyboard()
    else:
        markup = ReplyKeyboardRemove()
    await bot.send_message(
        user_id,
        question,
        reply_markup=markup
    )

class TrainingScene(Scene, state="training"):
    @on.message.enter()
    async def on_enter(self, message: Message, state: FSMContext) -> None:
        if not message.from_user: return
        await message.answer("Режим тренировки!")
        await message.answer("Предмет?")
        await state.update_data(trainstate=TrainingState.subject)
        await update_user_activity(message.from_user.id)


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
        await state.update_data(trainstate=TrainingState.chatting)
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

        await ask_question(id, response, t.question_type) 
        await state.update_data(trainstate=TrainingState.scoring)


    # chatting state, if asked for next question, we go to scoring state
    @on.message(Substate("trainstate", TrainingState.chatting))
    async def handle_chat(self, message: Message, state: FSMContext) -> None:
        print("chatting")
        if not message.from_user or not message.text: return

        id = message.from_user.id 
        response = await llm_client.use(
            history=message_history[id],
            proompt=message.text
        )
        qtype = (await state.get_data())["qtype"]
        await update_user_activity(message.from_user.id)

        if "Следующий вопрос" in message.text or "следующий вопрос" in message.text:
            await ask_question(id, response, qtype) 
            await state.update_data(trainstate=TrainingState.scoring)
        else:
            await message.answer(response, reply_markup=train_keyboard())


    # the next message will be treated as an answer to the question
    @on.message(Substate("trainstate", TrainingState.scoring))
    async def score(self, message: Message, state: FSMContext):
        print("scoring")
        if not message.from_user or not message.text: return

        id = message.from_user.id 
        response = await llm_client.use(
            history=message_history[id],
            proompt=message.text
        )
        await message.answer(response, reply_markup=train_keyboard())
        await state.update_data(trainstate=TrainingState.chatting)


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

