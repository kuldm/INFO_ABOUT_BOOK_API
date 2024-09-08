from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database import async_session_maker
from exceptions import AuthorAlreadyExistException, AuthorAbsentException
from models.authors import Author
from services.base import BaseService


class AuthorService(BaseService):
    model = Author

    @classmethod
    async def existing_author_id(cls, session: AsyncSession, id: int):
        # Проверка существования тэга по id
        existing_tag_id = await session.execute(select(cls.model).where(cls.model.id == id))
        return existing_tag_id.scalar()

    @classmethod
    async def existing_author_name(cls, session: AsyncSession, name: str):
        # Проверка существования тэга по имени
        existing_tag_name = await session.execute(select(cls.model).where(cls.model.name == name))
        return existing_tag_name.scalar()

    @classmethod
    async def add(cls, session: AsyncSession, name: str):
        # Проверка существования тэга по имени
        if await cls.existing_author_name(session, name):
            raise AuthorAlreadyExistException
        return await super().add(session, name=name)

    @classmethod
    async def update(cls, session: AsyncSession, id: int, name: str):
        # Проверка существования тэга по id
        if not await cls.existing_author_id(session, id):
            raise AuthorAbsentException
        if await cls.existing_author_name(session, name):
            raise AuthorAlreadyExistException
        return await super().update(session, id=id, name=name)

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, id: int):
        if not await cls.existing_author_id(session, id):
            raise AuthorAbsentException
        return await super().find_one_or_none(session, id=id)

    @classmethod
    async def delete(cls, session: AsyncSession, id: int):
        if not await cls.existing_author_id(session, id):
            raise AuthorAbsentException
        return await super().delete(session, id=id)
