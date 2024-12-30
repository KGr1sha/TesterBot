from .setup import connection
from .models import User 
from sqlalchemy import Result, delete, select
from typing import Optional
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


@connection
async def set_user(session: AsyncSession, tg_id: int, username: str, education: str) -> Optional[User]:
    try:
        user = await session.scalar(select(User).filter_by(id=tg_id))

        if not user:
            new_user = User(id=tg_id, username=username, education=education)
            session.add(new_user)
            await session.commit()
            return None
        else:
            return user

    except SQLAlchemyError as e:
        print(f"ERROR: {e}")
        await session.rollback()


@connection
async def get_user(session: AsyncSession, tg_id: int) -> Optional[User]:
    try:
        user = await session.scalar(select(User).filter_by(id=tg_id))
        return user

    except SQLAlchemyError as e:
        print(f"ERROR: {e}")
        await session.rollback()


@connection
async def get_users(session: AsyncSession):
    try:
        result: Result = await session.execute(select(User))
        users = result.scalars().all()
        return users

    except SQLAlchemyError as e:
        print(f"ERROR: {e}")
        await session.rollback()


@connection
async def delete_users(session: AsyncSession) -> int:
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
