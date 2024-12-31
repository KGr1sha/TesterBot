from .setup import connection
from .models import Test, User 
from sqlalchemy import Result, delete, select
from typing import Optional
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from .models import TestStruct


@connection
async def set_user(tg_id: int, username: str, education: str, session: AsyncSession=AsyncSession()) -> Optional[User]:
    try:
        user = await session.scalar(select(User).filter_by(id=tg_id))

        if not user:
            new_user = User(id=tg_id, username=username, education=education)
            session.add(new_user)
            await session.commit()
            return None

        return user

    except SQLAlchemyError as e:
        print(f"ERROR: {e}")
        await session.rollback()


@connection
async def get_user(tg_id: int, session: AsyncSession=AsyncSession()) -> Optional[User]:
    try:
        user = await session.scalar(select(User).filter_by(id=tg_id))
        return user

    except SQLAlchemyError as e:
        print(f"ERROR: {e}")
        await session.rollback()


@connection
async def get_users(session: AsyncSession=AsyncSession()):
    try:
        result: Result = await session.execute(select(User))
        users = result.scalars().all()
        return users

    except SQLAlchemyError as e:
        print(f"ERROR: {e}")
        await session.rollback()


@connection
async def delete_all_users(session: AsyncSession=AsyncSession()) -> int:
    try:
        result: Result = await session.execute(select(User))
        users = result.scalars().all()
        cnt = len(users)
        await session.execute(delete(User))
        await session.commit()
        return cnt
    except SQLAlchemyError as e:
        print(f"ERROR: {e}")
        await session.rollback()

    return 0


@connection
async def add_test(user_id: int, test: TestStruct, session: AsyncSession=AsyncSession()) -> Optional[Test]:
    try:
        user = await get_user(user_id)

        if not user:
            raise Exception("ERROR: USER IS NOT PRESENT, CAN'T ADD TEST")

        new_test = Test(
            user_id=user_id,
            subject=test.subject,
            theme=test.theme,
            number_of_questions=test.number_of_questions,
            question_type=test.question_type,
            difficulty=test.difficulty,
            time=test.time
        )

        session.add(new_test)
        await session.commit()
        return new_test

    except SQLAlchemyError as e:
        print(f"ERROR: {e}")
        await session.rollback()


@connection
async def get_tests(user_id: int, session: AsyncSession=AsyncSession()) -> Optional[list[TestStruct]]:
    try:
        result = await session.execute(select(Test).filter_by(user_id=user_id))
        tests = result.scalars().all()

        if not tests:
            print(f"No tests for user {user_id}")
            return list()

        test_list = [
            TestStruct(
                subject = test.subject,
                theme=test.theme,
                number_of_questions=test.number_of_questions,
                question_type=test.question_type,
                difficulty=test.difficulty,
                time=test.time,
            ) for test in tests
        ]

        return test_list


    except SQLAlchemyError as e:
        print(f"ERROR: {e}")
        await session.rollback()
