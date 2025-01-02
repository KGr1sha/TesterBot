from gigachat import use
from proompts import get_proompt
from database.models import TestStruct

class ProomptGenerator():
    def __init__(self, gigachat_token: str):
        self.token=gigachat_token

    async def generate_test(self, test_data: TestStruct) -> tuple[str, str]:
        proompt = get_proompt("create_test").format(
            subject=test_data.subject,
            theme=test_data.theme,
            number_of_questions=test_data.number_of_questions,
            question_type=test_data.question_type,
            difficulty=test_data.difficulty,
            time=test_data.time
        )

        response = await use(
            self.token,
            model="GigaChat",
            message_history=[],
            proompt=proompt
        )

        return response, proompt


    async def take_test(self, test_text: str) -> tuple[str, str]:
        proompt = get_proompt("take_test").format(
            test_content=test_text
        )

        response = await use(
            access_token=self.token,
            model="GigaChat",
            message_history=[],
            proompt=proompt 
        )

        return response, proompt

