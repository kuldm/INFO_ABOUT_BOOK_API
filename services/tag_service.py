from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions.exceptions import TagAlreadyExistException, TagAbsentException
from models.tags import Tag
from services.base import BaseService

from logger_config import logger


class TagService(BaseService):
    model = Tag

    @classmethod
    async def existing_tag_id(cls, session: AsyncSession, id: int):
        """Проверка существования тега по id"""
        existing_tag_id = await session.execute(select(cls.model).where(cls.model.id == id))
        return existing_tag_id.scalar()

    @classmethod
    async def existing_tag_name(cls, session: AsyncSession, name: str):
        """Проверка существования тега по имени"""
        existing_tag_name = await session.execute(select(cls.model).where(cls.model.name == name))
        return existing_tag_name.scalar()

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, id: int):
        """Поиск тега по идентификатору или создание исключения, если он не найден."""
        if not await cls.existing_tag_id(session, id):
            logger.warning(f"Tag with ID: {id} not found")
            raise TagAbsentException
        return await super().find_one_or_none(session, id=id)

    @classmethod
    async def add(cls, session: AsyncSession, name: str):
        """Добавление нового тега, если тег с таким названием не существует."""
        if await cls.existing_tag_name(session, name):
            logger.warning(f"Tag with name '{name}' already exists")
            raise TagAlreadyExistException
        return await super().add(session, name=name)

    @classmethod
    async def update(cls, session: AsyncSession, id: int, name: str):
        """Обновление существующего тега, если тег существует, а новое название не занято."""
        if not await cls.existing_tag_id(session, id):
            logger.warning(f"Tag with ID: {id} not found")
            raise TagAbsentException
        if await cls.existing_tag_name(session, name):
            logger.warning(f"Tag with name: '{name}' already exists")
            raise TagAlreadyExistException
        return await super().update(session, id=id, name=name)

    @classmethod
    async def delete(cls, session: AsyncSession, id: int):
        """Удаление тега по идентификатору, если он существует."""
        if not await cls.existing_tag_id(session, id):
            logger.warning(f"Tag with ID: {id} not found")
            raise TagAbsentException
        return await super().delete(session, id=id)
