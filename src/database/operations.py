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
async def add_test(user_id: int, test_settings: TestStruct, test_content: str, session: AsyncSession=AsyncSession()) -> Optional[Test]:
    try:
        user = await get_user(user_id)

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
            content_text=test_content
        )

        session.add(new_test)
        await session.commit()
        return new_test

    except SQLAlchemyError as e:
        print(f"ERROR: {e}")
        await session.rollback()



@connection
async def get_test(id: int, session: AsyncSession=AsyncSession()) -> Optional[Test]:
    try:
        test = await session.scalar(select(Test).filter_by(id=id))
        return test

    except SQLAlchemyError as e:
        print(f"ERROR: {e}")
        await session.rollback()


@connection
async def get_tests(user_id: int, session: AsyncSession=AsyncSession()) -> Optional[list]:
    try:
        result = await session.execute(select(Test).filter_by(user_id=user_id))
        tests = result.scalars().all()

        if not tests:
            print(f"No tests for user {user_id}")
            return list()

        test_list = [{
            "id": test.id,
            "settings": TestStruct(
                subject = test.subject,
                theme=test.theme,
                number_of_questions=test.number_of_questions,
                question_type=test.question_type,
                difficulty=test.difficulty,
                time=test.time,
            ),
            "content": test.content_text,
            "created_at": test.created_at,
        } for test in tests]
        

        return test_list


    except SQLAlchemyError as e:
        print(f"ERROR: {e}")
        await session.rollback()


@connection
async def delete_test(test_id: int, session: AsyncSession = AsyncSession()) -> None:
    try:
        await session.execute(delete(Test).where(Test.id==test_id))
        await session.commit()

    except SQLAlchemyError as e:
        print(f"ERROR: {e}")
        await session.rollback()

