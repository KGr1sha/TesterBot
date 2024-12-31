from proompts import get_proompt

print(
    get_proompt("create_test").format(
        subject="Матан",
        theme="Функции нескольких переменных",
        number_of_questions="3",
        question_type="Выбор вариантов",
        difficulty="Легкая",
        time="10 минут",
    )
)
