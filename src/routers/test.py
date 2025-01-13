from aiogram import Router, F
from aiogram.enums import content_type
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove
)
from aiogram.fsm.scene import Scene, on
from aiogram.fsm.context import FSMContext

from proompts import get_proompt
from states import TestCreation, Substate, TestingState
from database.operations import (
    add_test,
    delete_test,
    get_test,
    get_user,
    update_user_activity,
    update_user_form,
)
from database.models import TestData, Test
from proomptgen import ProomptGenerator
from setup import bot, llm_client 
from keyboards import (
    answers_keyboard,
    question_type_keyboard,
    number_of_questions_keyboard,
    time_keyboard,
    difficulty_keyboard,
    truefalse_keyboard
)
from timer import timer 
from parser import get_test_time, parse_answers, parse_questions, save_score

test_router = Router()

message_history = {}
timers = {}


class CreateTestScene(Scene, state="create_test"):
    @on.message.enter()
    async def on_enter(self, message: Message, state: FSMContext) -> None:
        if not message.from_user: return
        user = await get_user(message.from_user.id)
        if not user:
            await message.answer("Вы не зарегестрированы. Напишите /start")
            return
        await state.update_data(creation_state=TestCreation.subject)
        await message.answer("Создаем тест!")
        await message.answer("Предмет?")
        await update_user_activity(message.from_user.id)


    @on.message(Substate("creation_state", TestCreation.subject))
    async def handle_subject(self, message: Message, state: FSMContext) -> None:
        await state.update_data(subject=message.text)
        await state.update_data(creation_state=TestCreation.theme)
        await message.answer("Тема?")


    @on.message(Substate("creation_state", TestCreation.theme))
    async def handle_theme(self, message: Message, state: FSMContext) -> None:
        await state.update_data(theme=message.text)
        await state.update_data(creation_state=TestCreation.noq)
        await message.answer(
            "Сколько вопросов?",
            reply_markup=number_of_questions_keyboard()
        )

    
    @on.message(Substate("creation_state", TestCreation.noq))
    async def handle_noq(self, message: Message, state: FSMContext) -> None:
        await state.update_data(noq=message.text)
        await state.update_data(creation_state=TestCreation.qtype)
        await message.answer("Тип вопросов?", reply_markup=question_type_keyboard())


    @on.message(Substate("creation_state", TestCreation.qtype))
    async def handle_qtype(self, message: Message, state: FSMContext) -> None:
        await state.update_data(qtype=message.text)
        await state.update_data(creation_state=TestCreation.difficulty)
        await message.answer("Сложность?", reply_markup=difficulty_keyboard())


    @on.message(Substate("creation_state", TestCreation.difficulty))
    async def handle_difficultly(self, message: Message, state: FSMContext) -> None:
        await state.update_data(difficulty=message.text)
        await state.update_data(creation_state=TestCreation.time)
        await message.answer("Время на выполнение?(в минутах)", reply_markup=time_keyboard())


    @on.message(Substate("creation_state", TestCreation.time))
    async def handle_time(self, message: Message, state: FSMContext) -> None:
        if not message.from_user: return

        await state.update_data(time=message.text)
        data = await state.get_data()
        t = TestData(
            data["subject"],
            data["theme"],
            data["noq"],
            data["qtype"],
            data["difficulty"],
            data["time"],
        )
        sent = await message.answer("генерация теста...", reply_markup=ReplyKeyboardRemove())
        generator = ProomptGenerator()

        proompt = generator.create_test(t)
        test = await llm_client.use(proompt)

        added = await add_test(message.from_user.id, t, test)
        if not added:
            await message.answer("Ошибка при добавлении теста")
            return;

        await sent.delete()
        await message.answer("Тест добавлен!\nЧтобы пройти его используйте /take_test")
        await state.clear()


async def time_is_up(user_id: int):
    await bot.send_message(user_id, "Время вышло!\nДо свидания")


async def score_test(message: Message, state: FSMContext, scene: Scene):
    if not message.from_user or not message.text: return

    user_id = message.from_user.id
    test_id = int((await state.get_data())["test_id"])

    answers = (await state.get_data())["answers"]
    test = await get_test(test_id)
    if not test:
        raise Exception("paranormal behaviour")
    test_content = test.content_text
    proompt = ProomptGenerator().take_test(test_content, answers)

    response = await llm_client.use(
        history=[],
        proompt=proompt
    )

    await message.answer(response, reply_markup=ReplyKeyboardRemove())
    if not await save_score(response, user_id, test_id):
        await message.answer("Не удалось сохранить результат")

    task = timers[user_id]
    if not task.done():
        task.cancel()

    await update_user_activity(user_id)

    user = await get_user(user_id) # is not None
    if not user:
        raise Exception("Wow, something wierd happened, user can't be null here")
    if not user["filled_form"]:
        await state.update_data(substate=TestingState.filling_form)
        await message.answer("Поздравляю с прохождением первого теста!\nОставьте небольшой отзыв о работе бота🙏\nЭто поможет в его разработке")
    else:
        await scene.wizard.exit()


async def ask_question(user_id: int, test: Test, question_index: int):
    questions = parse_questions(test.content_text)
    question = questions[question_index]
    markup: ReplyKeyboardMarkup|ReplyKeyboardRemove
    
    if test.question_type == "С выбором вариантов ответа":
        markup = answers_keyboard(parse_answers(question))
    elif test.question_type == "Верно/неверно":
        markup = truefalse_keyboard()
    else:
        markup = ReplyKeyboardRemove()
    await bot.send_message(
        user_id,
        question,
        reply_markup=markup
    )

class TestingScene(Scene, state="testing"):
    @on.callback_query.enter()
    async def on_enter(self, query: CallbackQuery, state: FSMContext) -> None:
        if not query.data or not query.from_user: return
        user_id = query.from_user.id
        test_id = int(query.data)
        await state.update_data(test_id=test_id)
        test = await get_test(test_id)
        if not test:
            query.answer("Ошибка")
            return
        await query.message.edit_text("⌛️")

        await state.update_data(test=test)
        await state.update_data(question_number=0)
        await state.update_data(substate=TestingState.taking_test)
        await state.update_data(answers=list())

        await query.message.delete()
        await ask_question(user_id, test, 0)

        time = get_test_time(test.time)
        if time == -1: return
        task = timer(time_is_up, time * 60, args=[user_id])
        timers[user_id] = task
        await update_user_activity(user_id)

        
    @on.message(Substate("substate", TestingState.taking_test))
    async def handle_take_state(self, message: Message, state: FSMContext) -> None:
        if not message.from_user or not message.text: return
        d = await state.get_data()
        test: Test   = d["test"]
        question_num = d["question_number"] + 1
        answers      = d["answers"]
        answers.append(f"{question_num}: {message.text}")
        if question_num < len(parse_questions(test.content_text)):
            await ask_question(message.from_user.id, test, question_num)
            await state.update_data(question_number=question_num)
        else:
            await message.answer(
                "Вопросы кончились, перейдем к результатам...",
                reply_markup=ReplyKeyboardRemove()
            )
            hourglass = await message.answer("⌛️")
            await score_test(message, state, self)
            await hourglass.delete()


    @on.message(Substate("substate", TestingState.filling_form))
    async def fill_form(self, message: Message) -> None:
        if not message.from_user or not message.text: return
        user_id = message.from_user.id
        await update_user_form(user_id, message.text)
        await message.answer("Спасибо")



class DeletingTestScene(Scene, state="deleting_test"):
    @on.callback_query.enter()
    async def on_enter(self, query: CallbackQuery) -> None:
        if not query.data or not query.from_user: return
        test_id = int(query.data)
        await delete_test(test_id)
        await query.message.edit_text("Тест удален")


test_router.message.register(CreateTestScene.as_handler(), Command("create_test"))
test_router.callback_query.register(TestingScene.as_handler(), TestingState.selecting_take)
test_router.callback_query.register(DeletingTestScene.as_handler(), TestingState.selecting_delete)

