from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from config import settings

if settings.MODE == "TEST":
    DATABASE_URL = settings.TEST_DATABASE_URL
    DATABASE_PARAM = {"poolclass": NullPool}
else:
    DATABASE_URL = settings.DATABASE_URL
    DATABASE_PARAM = {}

# Создание асинхронного движка для базы данных
engine = create_async_engine(DATABASE_URL, **DATABASE_PARAM)

# Фабрика сессий
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncSession:
    """Асинхронный генератор сессий базы данных."""
    async with async_session_maker() as session:
        yield session


class Base(DeclarativeBase):
    pass
