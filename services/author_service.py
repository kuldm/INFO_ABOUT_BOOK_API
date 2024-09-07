from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database import async_session_maker
from exceptions import AuthorAlreadyExistException, AuthorAbsentException
from models.authors import Author
from services.base import BaseService


class AuthorService(BaseService):
    model = Author

    @classmethod
    async def existing_author_id(cls, id: int):
        async with async_session_maker() as session:
            # Проверка существования тэга по id
            existing_tag_id = await session.execute(select(cls.model).where(cls.model.id == id))
            return existing_tag_id.scalar()

    @classmethod
    async def existing_author_name(cls, name: str):
        async with async_session_maker() as session:
            # Проверка существования тэга по имени
            existing_tag_name = await session.execute(select(cls.model).where(cls.model.name == name))
            return existing_tag_name.scalar()

    @classmethod
    async def add(cls, name: str):
        # Проверка существования тэга по имени
        if await cls.existing_author_name(name):
            raise AuthorAlreadyExistException
        return await super().add(name=name)

    @classmethod
    async def update(cls, id: int, name: str):
        # Проверка существования тэга по id
        if not await cls.existing_author_id(id):
            raise AuthorAbsentException
        if await cls.existing_author_name(name):
            raise AuthorAlreadyExistException
        return await super().update(id=id, name=name)

    @classmethod
    async def find_one_or_none(cls, id: int):
        if not await cls.existing_author_id(id):
            raise AuthorAbsentException
        return await super().find_one_or_none(id=id)

    @classmethod
    async def delete(cls, id: int):
        if not await cls.existing_author_id(id):
            raise AuthorAbsentException
        return await super().delete(id=id)