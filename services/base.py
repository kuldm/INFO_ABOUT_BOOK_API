from sqlalchemy.orm import selectinload

from database import async_session_maker
from sqlalchemy import select, insert, delete


class BaseService:
    model = None

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).options(selectinload(cls.model.books)).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_all_books(cls, load_options=None, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            if load_options:
                # Применяем переданные опции для жадной загрузки, если они есть
                for option in load_options:
                    query = query.options(option)
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
    async def add_book(cls, title: str, author: str, tag: str):
        async with async_session_maker() as session:
            query = insert(cls.model).values(title).returning(cls.model.id, cls.model.name)
            query2 = insert()

    @classmethod
    async def delete(cls, **filter_by):
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(**filter_by)
            await session.execute(query)
            await session.commit()
