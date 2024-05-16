import contextlib
import typing
import loguru
import fastapi
from sqlalchemy.ext.asyncio import (
    async_sessionmaker as sqlalchemy_async_sessionmaker,
    AsyncSession as SQLAlchemyAsyncSession,
    AsyncSessionTransaction as SQLAlchemyAsyncSessionTransaction,
)

from src.repository.database import async_db


async def get_async_session() -> typing.AsyncGenerator[SQLAlchemyAsyncSession, None]:
    try:
        yield async_db.async_session
    except Exception as e:
        loguru.logger.info(f"Exception --- {e}")
        await async_db.async_session.rollback()
        raise
    finally:
        await async_db.async_session.close()
