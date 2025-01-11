from .database import async_session, engine, Base
from sqlalchemy.exc import SQLAlchemyError


def connection(func):
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            try:
                return await func(session=session, *args, **kwargs)
            except SQLAlchemyError as e:
                print(f"ERROR: {e}")
                await session.rollback()

    return wrapper


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
