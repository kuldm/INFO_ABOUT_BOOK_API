from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from exceptions import BookAbsentException, BookAlreadyExistException, AuthorsMissingException, TagsMissingException, \
    AuthorAbsentException, TagAbsentException
from models.authors import Author
from models.books import Book
from models.tags import Tag
from services.base import BaseService
from logger_config import logger


class BookService(BaseService):
    model = Book

    @classmethod
    async def find_all_books(cls, session: AsyncSession, author_id: Optional[int] = None, tag_id: Optional[int] = None):
        """Поиск всех книги с опциональной фильтрацией по автору и тегу."""
        load_options = [selectinload(cls.model.authors), selectinload(cls.model.tags)]
        # Формируем запрос
        query = select(cls.model)
        # Если author_id передан, фильтруем книги по автору
        if author_id:
            query = query.where(cls.model.authors).where(Author.id == author_id)
        # Если tag_id передан, фильтруем книги по тегу
        if tag_id:
            query = query.where(cls.model.tags).where(Tag.id == tag_id)

        if load_options:
            for option in load_options:
                query = query.options(option)

        # Выполняем запрос и возвращаем результат
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def add_book(cls, session: AsyncSession, name: str, authors: List[str], tags: List[str]):
        """Добавление новой книги с указанными авторами и тегами."""
        # Проверка на наличие авторов
        if not authors:
            logger.error("No authors provided for the book")
            raise AuthorsMissingException
        # Проверка на наличие тегов
        if not tags:
            logger.error("No tags provided for the book")
            raise TagsMissingException

        # Проверка существования книги
        existing_book = await session.execute(select(cls.model).where(cls.model.name == name))
        if existing_book.scalar():
            logger.warning(f"Book with name: '{name}' already exists")
            raise BookAlreadyExistException

        # Проверка авторов: если нет, то создать
        author_objects = []
        for author_name in authors:
            existing_author = await session.execute(select(Author).where(Author.name == author_name))
            author = existing_author.scalar()
            if not author:
                logger.error(f"Author '{author_name}' does not exist in the database")
                raise AuthorAbsentException
            author_objects.append(author)

        # Проверка теговЖ если нет то создать
        tags_objects = []
        for tag_name in tags:
            existing_tags = await session.execute(select(Tag).where(Tag.name == tag_name))
            tag = existing_tags.scalar()
            if not tag:
                logger.error(f"Tag '{tag_name}' does not exist in the database")
                raise TagAbsentException
            tags_objects.append(tag)

        # Создание книги
        new_book = Book(name=name)
        new_book.authors = author_objects
        new_book.tags = tags_objects

        session.add(new_book)
        await session.commit()
        await session.refresh(new_book)

        return {"id": new_book.id, "name": new_book.name}

    @classmethod
    async def update_book(cls, session: AsyncSession, book_id: int, name: str):
        """Обновляет название книги по ID."""
        # Проверка существования книги
        book = await session.execute(select(Book).where(Book.id == book_id))
        book = book.scalar()
        if not book:
            logger.warning(f"Book with ID: {book_id} not found")
            raise BookAbsentException

        existing_book = await session.execute(select(Book).where(Book.name == name, Book.id != book_id))
        if existing_book.scalar():
            logger.warning(f"Book with name: '{name}' already exists")
            raise BookAlreadyExistException
        book.name = name

        await session.commit()
        await session.refresh(book)

        return book

    @classmethod
    async def delete_book(cls, session: AsyncSession, book_id: int):
        """Удаляет книгу по ID."""
        # Поиск книги
        book = await session.execute(select(Book).where(Book.id == book_id))
        book = book.scalar()

        if not book:
            logger.warning(f"Book with ID {book_id} not found")
            raise BookAbsentException

        await session.delete(book)
        await session.commit()

        return {"Книга успешно удалена"}

    @classmethod
    async def find_one_or_none_book(cls, session: AsyncSession, id: int):
        """Находит одну книгу по ID с подгрузкой авторов и тегов."""
        load_options = [selectinload(cls.model.authors), selectinload(cls.model.tags)]
        # Проверка существования книги по имени
        existing_book_id = await session.execute(select(cls.model).where(cls.model.id == id))

        if not existing_book_id.scalar():
            logger.warning(f"Book with ID: {id} not found")
            raise BookAbsentException

        query = select(cls.model).filter(cls.model.id == id)

        if load_options:
            for option in load_options:
                query = query.options(option)

        result = await session.execute(query)
        return result.scalars().first()
