from typing import List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database import async_session_maker
from exceptions import BookAbsentException, BookAlreadyExistException, AuthorsMissingException, TagsMissingException
from models.authors import Author
from models.books import Book
from models.tags import Tag
from services.base import BaseService


class BookService(BaseService):
    model = Book

    @classmethod
    async def find_all_books(cls):
        async with async_session_maker() as session:
            load_options = [selectinload(cls.model.authors), selectinload(cls.model.tags)]
            # Формируем запрос
            query = select(cls.model)
            if load_options:
                for option in load_options:
                    query = query.options(option)

            # Выполняем запрос и возвращаем результат
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add_book(cls, name: str, authors: List[str], tags: List[str]):
        async with async_session_maker() as session:

            # Проверка на наличие авторов и тегов
            if not authors:
                raise AuthorsMissingException
            if not tags:
                raise TagsMissingException

            # Проверка существования книги
            existing_book = await session.execute(select(cls.model).where(cls.model.name == name))
            if existing_book.scalar():
                raise BookAlreadyExistException

            # Проверка авторов: если нет, то создать
            author_objects = []
            for author_name in authors:
                existing_author = await session.execute(select(Author).where(Author.name == author_name))
                author = existing_author.scalar()
                if not author:
                    author = Author(name=author_name)
                    session.add(author)
                author_objects.append(author)

            # Проверка теговЖ если нет то создать
            tags_objects = []
            for tag_name in tags:
                existing_tags = await session.execute(select(Tag).where(Tag.name == tag_name))
                tag = existing_tags.scalar()
                if not tag:
                    tag = Tag(name=tag_name)
                    session.add(tag)
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
    async def update_book(cls, book_id: int, name: str):
        async with async_session_maker() as session:

            # Проверка существования книги
            book = await session.execute(select(Book).where(Book.id == book_id))
            book = book.scalar()
            if not book:
                raise BookAbsentException

            existing_book = await session.execute(select(Book).where(Book.name == name, Book.id != book_id))
            if existing_book.scalar():
                raise BookAlreadyExistException
            book.name = name

            await session.commit()
            await session.refresh(book)

            return book

    @classmethod
    async def delete_book(cls, book_id: int):
        async with async_session_maker() as session:
            # Поиск книги
            book = await session.execute(select(Book).where(Book.id == book_id))
            book = book.scalar()

            if not book:
                raise BookAbsentException

            await session.delete(book)
            await session.commit()

            return {"Книга успешно удалена"}


    @classmethod
    async def find_one_or_none(cls, id: int):
        async with async_session_maker() as session:
            # Проверка существования книги по имени
            existing_book_id = await session.execute(select(cls.model).where(cls.model.id == id))
            if not existing_book_id.scalar():
                raise BookAbsentException
        return await super().find_one_or_none(id=id)
