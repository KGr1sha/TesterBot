from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=True)
    education: Mapped[str] = mapped_column(String, nullable=True)

    def __str__(self) -> str:
        return f"{self.id} | {self.username} | {self.education}"
