from sqlalchemy import select

from database import async_session_maker
from exceptions import TagAlreadyExistException, TagAbsentException
from models.tags import Tag
from services.base import BaseService


class TagService(BaseService):
    model = Tag

    @classmethod
    async def existing_tag_id(cls, id: int):
        async with async_session_maker() as session:
            # Проверка существования тэга по id
            existing_tag_id = await session.execute(select(cls.model).where(cls.model.id == id))
            return existing_tag_id.scalar()

    @classmethod
    async def existing_tag_name(cls, name: str):
        async with async_session_maker() as session:
            # Проверка существования тэга по имени
            existing_tag_name = await session.execute(select(cls.model).where(cls.model.name == name))
            return existing_tag_name.scalar()

    @classmethod
    async def add(cls, name: str):
        # Проверка существования тэга по имени
        if await cls.existing_tag_name(name):
            raise TagAlreadyExistException
        return await super().add(name=name)

    @classmethod
    async def update(cls, id: int, name: str):
        # Проверка существования тэга по id
        if not await cls.existing_tag_id(id):
            raise TagAbsentException
        if await cls.existing_tag_name(name):
            raise TagAlreadyExistException
        return await super().update(id=id, name=name)

    @classmethod
    async def find_one_or_none(cls, id: int):
        if not await cls.existing_tag_id(id):
            raise TagAbsentException
        return await super().find_one_or_none(id=id)

    @classmethod
    async def delete(cls, id: int):
        if not await cls.existing_tag_id(id):
            raise TagAbsentException
        return await super().delete(id=id)