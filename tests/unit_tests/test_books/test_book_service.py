import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions import BookAbsentException
from services.book_service import BookService


@pytest.mark.parametrize("book_id,book_exists", [
    (1, True),
    (110, False),
])
async def test_find_book_by_id(session: AsyncSession, book_id: int, book_exists: bool):
    if book_exists:
        book = await BookService.find_one_or_none_book(session, id=book_id)
        assert book
        assert book.id == book_id
    else:
        with pytest.raises(BookAbsentException):
            await BookService.find_one_or_none_book(session, id=book_id)
