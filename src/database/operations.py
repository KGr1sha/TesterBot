from .setup import connection
from .models import Test, User 
from sqlalchemy import Result, delete, func, select
from typing import Optional
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from .models import TestData


@connection
async def set_user(tg_id: int, username: str, education: str, session: AsyncSession=AsyncSession()) -> Optional[User]:
    user = await session.scalar(select(User).filter_by(id=tg_id))

    if not user:
        new_user = User(
            id=tg_id,
            username=username,
            education=education,
            right_answers=0,
            total_answers=0
        )
        session.add(new_user)
        await session.commit()
        return None

    return user


@connection
async def get_user(tg_id: int, session: AsyncSession=AsyncSession()) -> Optional[dict]:
    user = await session.scalar(select(User).filter_by(id=tg_id))
    if not user:
        return None

    user_dict = {
        "id": user.id,
        "name": user.username,
        "education": user.education,
        "last_activity": user.last_activity,
        "total_answers": user.total_answers,
        "right_answers": user.right_answers,
        "filled_form": user.filled_form
    }
    return user_dict


@connection
async def get_users(session: AsyncSession=AsyncSession()) -> list[User]:
    result: Result = await session.execute(select(User))
    users = result.scalars().all()
    return users


@connection
async def add_user_statistics(user_id: int, add_right_answers: int, add_total_answers: int, session: AsyncSession=AsyncSession()) -> Optional[User]:
    user = await session.scalar(select(User).filter_by(id=user_id))
    if not user:
        return None
    user.right_answers += add_right_answers
    user.total_answers += add_total_answers
    await session.commit()
    return user


@connection
async def update_user_form(user_id: int, filled_text: str, session: AsyncSession=AsyncSession()) -> Optional[User]:
    user = await session.scalar(select(User).filter_by(id=user_id))
    if not user: return None

    user.filled_form = True
    user.form_text = filled_text

    await session.commit()
    return user

@connection
async def update_user_activity(user_id: int, session: AsyncSession=AsyncSession()):
    user = await session.scalar(select(User).filter_by(id=user_id))
    if not user: return
    user.last_activity = func.now()
    await session.commit()


@connection
async def add_test(user_id: int, test_settings: TestData, test_content: str, session: AsyncSession=AsyncSession()) -> Optional[Test]:
    user = await session.scalar(select(User).filter_by(id=user_id))

    if not user:
        return None

    new_test = Test(
        user_id=user_id,
        subject=test_settings.subject,
        theme=test_settings.theme,
        number_of_questions=test_settings.number_of_questions,
        question_type=test_settings.question_type,
        difficulty=test_settings.difficulty,
        time=test_settings.time,
        content_text=test_content,
        last_score=""
    )

    session.add(new_test)
    await session.commit()
    return new_test


@connection
async def update_test_score(test_id: int, new_score: str, session: AsyncSession=AsyncSession()) -> Optional[Test]:
    test = await session.scalar(select(Test).filter_by(id=test_id))
    if (not test):
        return None;
    
    test.last_score = new_score
    await session.commit()
    return test
    

@connection
async def get_test(id: int, session: AsyncSession=AsyncSession()) -> Optional[Test]:
    test = await session.scalar(select(Test).filter_by(id=id))
    return test


@connection
async def get_tests(user_id: int, session: AsyncSession=AsyncSession()) -> Optional[list]:
    result = await session.execute(select(Test).filter_by(user_id=user_id))
    tests = result.scalars().all()

    if not tests:
        print(f"No tests for user {user_id}")
        return list()

    test_list = [{
        "id": test.id,
        "settings": TestData(
            subject = test.subject,
            theme=test.theme,
            number_of_questions=test.number_of_questions,
            question_type=test.question_type,
            difficulty=test.difficulty,
            time=test.time,
        ),
        "content": test.content_text,
        "created_at": test.created_at,
        "last_score": test.last_score
    } for test in tests]
    
    return test_list


@connection
async def delete_test(test_id: int, session: AsyncSession = AsyncSession()) -> None:
    await session.execute(delete(Test).where(Test.id==test_id))
    await session.commit()
