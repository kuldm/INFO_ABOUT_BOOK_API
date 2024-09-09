import asyncio
import json

import pytest
from sqlalchemy import insert, text

from fastapi.testclient import TestClient
from httpx import AsyncClient

from config import settings
from database import Base, async_session_maker, engine

from models.tags import Tag
from models.authors import Author
from models.books import Book
from models.users import Users
from main import app as fastapi_app


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"tests/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)

    tags = open_mock_json("tags")
    authors = open_mock_json("authors")
    books = open_mock_json("books")
    users = open_mock_json("users")
    book_author_data = open_mock_json("book_author")
    book_tag_data = open_mock_json("book_tag")

    async with async_session_maker() as session:
        add_tags = insert(Tag).values(tags)
        add_authors = insert(Author).values(authors)
        add_books = insert(Book).values(books)
        add_users = insert(Users).values(users)

        await session.execute(add_tags)
        await session.execute(add_authors)
        await session.execute(add_books)
        await session.execute(add_users)

        for record in book_tag_data:
            sql = """
                INSERT INTO book_tag (book_id, tag_id)
                VALUES (:book_id, :tag_id)
            """
            await session.execute(text(sql), {
                "book_id": record['book_id'],
                "tag_id": record['tag_id']
            })

        for record in book_author_data:
            sql = """
                INSERT INTO book_author (book_id, author_id)
                VALUES (:book_id, :author_id)
            """
            await session.execute(text(sql), {
                "book_id": record['book_id'],
                "author_id": record['author_id']
            })
        await session.commit()


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def session():
    async with async_session_maker() as session:
        yield session
