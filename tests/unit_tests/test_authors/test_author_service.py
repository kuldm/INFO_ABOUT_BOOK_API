import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions.exceptions import AuthorAbsentException, AuthorAlreadyExistException

from services.author_service import AuthorService


@pytest.mark.parametrize("author_id,author_exists", [
    (1, True),
    (33, False),
])
async def test_find_author_by_id(session: AsyncSession, author_id: int, author_exists: bool):
    if author_exists:
        author = await AuthorService.find_one_or_none(session, id=author_id)
        assert author
        assert author.id == author_id
    else:
        with pytest.raises(AuthorAbsentException):
            await AuthorService.find_one_or_none(session, id=author_id)


@pytest.mark.parametrize("author_name,author_exists", [
    ("Дарья Донцов", True),
    ("Калягин", False),
])
async def test_add_author_by_name(session: AsyncSession, author_name: str, author_exists: bool):
    if author_exists:
        with pytest.raises(AuthorAlreadyExistException):
            await AuthorService.add(session, name=author_name)
    else:
        result = await AuthorService.add(session, name=author_name)
        assert result is not None
        assert result['name'] == author_name
