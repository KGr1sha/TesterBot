from dataclasses import dataclass

from sqlalchemy import BigInteger, Integer, String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base

@dataclass
class TestStruct:
    subject: str
    theme: str
    number_of_questions: str
    question_type: str
    difficulty: str
    time: str


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=True)
    education: Mapped[str] = mapped_column(String, nullable=True)

    tests: Mapped[list["Test"]] = relationship(
        "Test",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __str__(self) -> str:
        return f"{self.id} | {self.username} | {self.education}"


class Test(Base):
    __tablename__ = 'tests'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)

    subject: Mapped[str] = mapped_column(String, nullable=True)
    theme: Mapped[str] = mapped_column(String, nullable=True)
    number_of_questions: Mapped[str] = mapped_column(String, nullable=True)
    question_type: Mapped[str] = mapped_column(String, nullable=True)
    difficulty: Mapped[str] = mapped_column(String, nullable=True)
    time: Mapped[str] = mapped_column(String, nullable=True)
    content_text: Mapped[str] = mapped_column(Text, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="tests")

    def __str__(self) -> str:
        return f"""subject: {self.subject}
        theme: {self.theme}
        questions: {self.number_of_questions} {self.question_type} {self.difficulty}
        timie: {self.time}"""

