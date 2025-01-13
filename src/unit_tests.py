from routers.test import get_test_time
from parser import parse_answers, parse_questions

def test_get_time():
    assert get_test_time("5 minuytes") == 5
    assert get_test_time("минут 5") == 5
    assert get_test_time("ми5нут") == 5
    assert get_test_time("ми55нут") == 55
    assert get_test_time("минууутминууут") == -1


def test_parse_questions():
    test_text = \
"""
===
1 вопрос:
Какой из компонентов является наиболее важным для инициации взрыва в большинстве типов бомб?

a) Взрыватель
b) Взрывчатое вещество
c) Корпус бомбы
d) Детонатор

===
2 вопрос:
Что является наиболее распространенным типом взрывчатого вещества, используемого в самодельных бомбах?

a) Тринитротолуол (TNT)
b) Пластиковая взрывчатка C4
c) Аммиачная селитра
d) Динамит

===
3 вопрос:
Какая из следующих мер безопасности наименее эффективна при обращении с компонентами для создания бомбы?

a) Работа в хорошо вентилируемом помещении.
b) Использование защитных очков и перчаток.
c) Хранение компонентов в одном месте для удобства.
d) Избегание смешивания компонентов до непосредственного использования.
===
"""
    questions = parse_questions(test_text)
    for i in range(len(questions)):
        print(f"==={i}===\n{questions[i]}")


def test_parse_answers():
    question_txt = """
===
1 вопрос:
Какой из компонентов является наиболее важным для инициации взрыва в большинстве типов бомб?

a) Взрыватель
b) Взрывчатое вещество
c) Корпус бомбы
d) Детонатор
"""
    answers = parse_answers(question_txt)
    for i in range(len(answers)):
        print(f"{i} -- {answers[i]}")



def run_tests():
    test_get_time()
    test_parse_questions()
    # test_parse_answers()

if __name__ == "__main__":
    run_tests()
