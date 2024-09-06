from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database import async_session_maker
from models.books import Book
from services.base import BaseService


class BookService(BaseService):
    model = Book

    @classmethod
    async def find_all_books(cls, **filter_by):
        # Указываем жадную загрузку авторов и тегов для модели Book
        load_options = [selectinload(cls.model.authors), selectinload(cls.model.tags)]
        return await super().find_all_books(load_options=load_options, **filter_by)