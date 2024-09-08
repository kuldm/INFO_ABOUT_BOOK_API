from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.postgresql.asyncpg import AsyncAdapt_asyncpg_dbapi

from database import async_session_maker
from exceptions import LinkM2MException, UserIsNotPresentException
from models.users import Users
from services.base import BaseService
from logger_config import logger


class UserService(BaseService):
    model = Users

    @classmethod
    async def find_user(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def add_user(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data).returning(cls.model.id, cls.model.username)
            result = await session.execute(query)
            await session.commit()
            return result.mappings().first()

    @classmethod
    async def delete_user(cls, username:str):
        async with async_session_maker() as session:
            existing_book_id = await session.execute(select(cls.model).where(cls.model.username == username))
            if not existing_book_id.scalar():
                logger.error(f"The user with id: {username} does not exist")
                raise UserIsNotPresentException
            try:
                query = delete(cls.model).filter(cls.model.username == username)
                await session.execute(query)
                await session.commit()
            except IntegrityError as e:
                # Проверяем, является ли ошибка нарушением ограничения внешнего ключа
                if isinstance(e.orig, AsyncAdapt_asyncpg_dbapi.IntegrityError) and 'ForeignKeyViolationError' in str(
                        e.orig):
                    raise LinkM2MException
        # return {"Запись успешно удалена"}
