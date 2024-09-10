from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions import AuthorAlreadyExistException, AuthorAbsentException
from models.authors import Author
from services.base import BaseService
from logger_config import logger
from utils.elasticsearch_utils import index_document, search, delete_document


class AuthorService(BaseService):
    model = Author
    es_index = 'tags'

    @classmethod
    async def existing_author_id(cls, session: AsyncSession, id: int):
        """Проверка существования автора по id"""
        existing_tag_id = await session.execute(select(cls.model).where(cls.model.id == id))
        return existing_tag_id.scalar()

    @classmethod
    async def existing_author_name(cls, session: AsyncSession, name: str):
        """Проверка существования автора по имени"""
        existing_tag_name = await session.execute(select(cls.model).where(cls.model.name == name))
        return existing_tag_name.scalar()

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, id: int):
        """Поиск автора по идентификатору или создание исключения, если он не найден."""
        if not await cls.existing_author_id(session, id):
            logger.warning(f"Author with ID: {id} not found")
            raise AuthorAbsentException
        return await super().find_one_or_none(session, id=id)

    @classmethod
    async def add(cls, session: AsyncSession, name: str):
        """Добавление нового автора, если автор с таким именем не существует."""
        if await cls.existing_author_name(session, name):
            logger.warning(f"Author with name: '{name}' already exists")
            raise AuthorAlreadyExistException
        author = await super().add(session, name=name)
        index_document(cls.es_index, 'tag', author['id'], {'name': author['name']})
        return author

    @classmethod
    async def update(cls, session: AsyncSession, id: int, name: str):
        """Обновление существующего автора, если автор существует, а новое имя не занято."""
        if not await cls.existing_author_id(session, id):
            logger.warning(f"Author with ID: {id} not found")
            raise AuthorAbsentException
        if await cls.existing_author_name(session, name):
            logger.warning(f"Author with name: '{name}' already exists")
            raise AuthorAlreadyExistException
        author = await super().update(session, id=id, name=name)
        index_document(cls.es_index, 'tag', author['id'], {'name': author['name']})
        return author

    @classmethod
    async def delete(cls, session: AsyncSession, id: int):
        """Удаление автора по идентификатору, если он существует."""
        if not await cls.existing_author_id(session, id):
            logger.warning(f"Author with ID: {id} not found")
            raise AuthorAbsentException
        result = await super().delete(session, id=id)
        delete_document(cls.es_index, 'author', id)
        return result

    @classmethod
    async def search_authors(cls, query: str):
        """Поиск авторов в Elasticsearch."""
        return search(cls.es_index, query)
