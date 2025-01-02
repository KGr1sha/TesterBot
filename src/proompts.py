test_proompts = {
    "create_test": """Мне нужно проверить свои знания.
Составь для меня тест. Вот характеристики теста:
Предмет: {subject};
Тема: {theme};
Количество вопросов: {number_of_questions};
Тип вопросов: {question_type};
Сложность: {difficulty};
Рассчитанное время: {time}.

ОЧЕНЬ ВАЖНО: ПРИШЛИ ТЕСТ БЕЗ ОТВЕТОВ""",

    "take_test": """Ты проводишь тест,
который состоит из нескольких вопросов.
Ты должен принимать мои ответы
на каждый вопрос и оценивать,
насколько ответы правильные.

Придумывать тест не надо. Он уже есть.
Достаточно просто проверять мои ответы.
Вот сам тест, который ты проводишь:
{test_content}""",
}

def get_proompt(key: str) -> str:
    return test_proompts[key]
