test_proompts = {
    "create_test": """Мне нужно проверить свои знания.
Составь для меня тест. Вот характеристики теста:
Предмет: {subject};
Тема: {theme};
Количество вопросов: {number_of_questions};
Тип вопросов: {question_type};
Сложность: {difficulty};
Рассчитанное время: {time}.
Важно: не показывай мне ответы.""",
}

def get_proompt(key: str) -> str:
    return test_proompts[key]
