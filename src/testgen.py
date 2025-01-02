from proompts import get_proompt
from database.models import TestStruct

class ProomptGenerator():
    def create_test(self, test_data: TestStruct) -> str:
        proompt = get_proompt("create_test").format(
            subject=test_data.subject,
            theme=test_data.theme,
            number_of_questions=test_data.number_of_questions,
            question_type=test_data.question_type,
            difficulty=test_data.difficulty,
            time=test_data.time
        )

        return proompt


    def take_test(self, test_text: str) -> str:
        proompt = get_proompt("take_test").format(
            test_content=test_text
        )

        return proompt

