from proompts import get_proompt
from database.models import TestData, TrainingData

class ProomptGenerator():
    def create_test(self, test_data: TestData) -> str:
        return get_proompt("create_test").format(
            subject=test_data.subject,
            theme=test_data.theme,
            number_of_questions=test_data.number_of_questions,
            question_type=test_data.question_type,
            difficulty=test_data.difficulty,
            time=test_data.time
        )


    def take_test(self, test_text: str, answers: list[str]) -> str:
        return get_proompt("take_test").format(
            test_content=test_text,
            answers = "\n".join(answers)
        )

    
    def train(self, training_data: TrainingData) -> str:
        return get_proompt("train").format(
            subject=training_data.subject,
            theme=training_data.theme,
            question_type=training_data.question_type,
            difficulty=training_data.difficulty
        )

