from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup


def answers_keyboard(answers: list[str]):
    builder = ReplyKeyboardBuilder()
    for a in answers:
        builder.button(text=a)
    builder.adjust(1, True)
    return builder.as_markup(resize_keyboard=True)


def truefalse_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Верно")
    builder.button(text="Неверно")
    builder.adjust(1, True)
    return builder.as_markup(resize_keyboard=True)


def education_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="Основное общее (9 класс)")
    builder.button(text="Среднее общее (11 класс)")
    builder.button(text="Среднее профессиональное")
    builder.button(text="Высшее")
    builder.adjust(1, True)
    return builder.as_markup(resize_keyboard=True)


def number_of_questions_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="3")
    builder.button(text="5")
    builder.button(text="10")
    builder.adjust(1, True)
    return builder.as_markup(resize_keyboard=True)


def question_type_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="С выбором вариантов ответа")
    builder.button(text="Открытый")
    builder.button(text="Верно/неверно")
    builder.adjust(1, True)
    return builder.as_markup(resize_keyboard=True)


def difficulty_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="Легко")
    builder.button(text="Средне")
    builder.button(text="Сложно")
    builder.adjust(1, True)
    return builder.as_markup(resize_keyboard=True)


def time_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="5 минут")
    builder.button(text="15 минут")
    builder.button(text="30 минут")
    builder.adjust(1, True)
    return builder.as_markup(resize_keyboard=True)


def train_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="Следующий вопрос")
    builder.button(text="Объясни")
    builder.button(text="Закончить тренировку")
    builder.adjust(2, 1)
    return builder.as_markup(resize_keyboard=True)


