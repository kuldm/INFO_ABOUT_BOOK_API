import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions import TagAbsentException, TagAlreadyExistException, LinkM2MException
from services.tag_service import TagService


@pytest.mark.parametrize("tag_id,tag_exists", [
    (1, True),
    (110, False),
])
async def test_find_tag_by_id(session: AsyncSession, tag_id: int, tag_exists: bool):
    if tag_exists:
        tag = await TagService.find_one_or_none(session, id=tag_id)
        assert tag
        assert tag.id == tag_id
    else:
        with pytest.raises(TagAbsentException):
            await TagService.find_one_or_none(session, id=tag_id)


@pytest.mark.parametrize("tag_name,tag_exists", [
    ("Бестселлер", True),
    ("Эпос", False),
])
async def test_add_tag_by_name(session: AsyncSession, tag_name: str, tag_exists: bool):
    if tag_exists:
        with pytest.raises(TagAlreadyExistException):
            await TagService.add(session, name=tag_name)
    else:
        result = await TagService.add(session, name=tag_name)
        assert result is not None
        assert result['name'] == tag_name


@pytest.mark.parametrize("tag_id,tag_exists,tag_m2m", [
    (100, False, False),
    (1, True, True),
])
async def test_delete_tag_by_id(session: AsyncSession, tag_id: int, tag_exists: bool, tag_m2m: bool):
    if tag_exists:
        # Проверяем, что тег существует перед удалением
        tag = await TagService.find_one_or_none(session, id=tag_id)
        assert tag is not None
        assert tag.id == tag_id

        if tag_m2m:
            # Если тег связан с другими записями, проверяем, что выбрасывается LinkM2MException
            with pytest.raises(LinkM2MException):
                await TagService.delete(session, id=tag_id)
    else:
        # Проверяем, что попытка удаления несуществующего тега вызывает исключение
        with pytest.raises(TagAbsentException):
            await TagService.delete(session, id=tag_id)
