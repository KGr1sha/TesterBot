# Бот для составления вопросов и тестов!
### [ссылка на бота](https://t.me/testsproject_bot)

## Возможности
* Составление тестов по указаным параметрам
* Прохождение тестов(проверка ответов и объяснение)
* Режим тренировки - бесконечный тест по указаным параметрам
* Учет статистики правильных ответов
* Напоминания о прохождении тестов

---
### Как работает
#### Стек
* asyncio
* aiogram
* aiohttp
* sqlalchemy
* sqlite
* LLM API (GigaChat/Gemini/ChatGPT)

#### Использование LLM
Бот поддерживает API Gigachat, Gemini(используется сейчас) и ChatGPT.
LLM использутеся для генерации тестов, их проверки и проведения тренировки.
Промты находятся [здесь](src/proompts.py)

---
### Скриншоты

<p>
  <img title="Создание теста" align=left width=400 height=600 src=https://github.com/user-attachments/assets/28896520-e18b-40b0-acb4-09c4573fcc84>
  <img title="Выбор теста" align=right width=550 height=250 vspace=20 src=https://github.com/user-attachments/assets/35f1cbf6-dd43-478a-b4b6-c5fe7432595f>
  <img title="Прохождение теста" align=left width=550 height=450 vspace=20 src=https://github.com/user-attachments/assets/79ce4eaf-24cd-4329-aca3-a4331edc9b4c>  
  <img width=600 height=250 src=https://github.com/user-attachments/assets/c7fc770d-adaa-418c-84dc-4407945657ef>
  <img width=450 height=600 src=https://github.com/user-attachments/assets/f23edebf-6593-46c3-8fd3-3438dfdac335>
  <img width=500 height=600 src=https://github.com/user-attachments/assets/945823ff-dcc7-40c2-b770-994cbf2c6048>


</p>




