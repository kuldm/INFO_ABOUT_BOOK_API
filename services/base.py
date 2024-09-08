from sqlalchemy.orm import selectinload

from database import async_session_maker
from sqlalchemy import select, insert, delete, update, func

from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.postgresql.asyncpg import AsyncAdapt_asyncpg_dbapi

from exceptions import LinkM2MException


class BaseService:
    model = None

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).options(selectinload(cls.model.books)).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data).returning(cls.model.id, cls.model.name)
            result = await session.execute(query)
            await session.commit()
            return result.mappings().first()

    @classmethod
    async def update(cls, id: int, name: str):
        async with async_session_maker() as session:
            query = update(cls.model).where(cls.model.id == id).values(name=name).returning(cls.model.id,
                                                                                            cls.model.name)

            result = await session.execute(query)
            await session.commit()
            return result.mappings().first()

    @classmethod
    async def delete(cls, **filter_by):
        async with async_session_maker() as session:
            try:
                query = delete(cls.model).filter_by(**filter_by)
                await session.execute(query)
                await session.commit()
            except IntegrityError as e:
                # Проверяем, является ли ошибка нарушением ограничения внешнего ключа
                if isinstance(e.orig, AsyncAdapt_asyncpg_dbapi.IntegrityError) and 'ForeignKeyViolationError' in str(
                        e.orig):
                    raise LinkM2MException
        return {"Запись успешно удалена"}


    # @classmethod
    # async def add(cls, **data):
    #     async with async_session_maker() as session:
    #         query = insert(cls.model).values(**data)#.returning(cls.model.id, cls.model.name)
    #         await session.execute(query)
    #         await session.commit()
