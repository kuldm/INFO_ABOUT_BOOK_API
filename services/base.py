import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, insert, delete, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.postgresql.asyncpg import AsyncAdapt_asyncpg_dbapi

from exceptions import LinkM2MException

logger = logging.getLogger(__name__)


class BaseService:
    model = None

    @classmethod
    async def find_all(cls, session: AsyncSession, **filter_by):
        """Извлекает все записи, соответствующие фильтру."""
        query = select(cls.model).options(selectinload(cls.model.books)).filter_by(**filter_by)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, **filter_by):
        """Извлекает одну запись, соответствующую фильтру, или возвращает None."""
        query = select(cls.model.__table__.columns).filter_by(**filter_by)
        result = await session.execute(query)
        return result.mappings().one_or_none()

    @classmethod
    async def add(cls, session: AsyncSession, **data):
        """Добавляет новую запись и возвращает созданную запись."""
        query = insert(cls.model).values(**data).returning(cls.model.id, cls.model.name)
        result = await session.execute(query)
        await session.commit()
        return result.mappings().first()

    @classmethod
    async def update(cls, session: AsyncSession, id: int, name: str):
        """Обновляет запись по ID и возвращает обновленную запись."""
        query = update(cls.model).where(cls.model.id == id).values(name=name).returning(cls.model.id,
                                                                                        cls.model.name)

        result = await session.execute(query)
        await session.commit()
        return result.mappings().first()

    @classmethod
    async def delete(cls, session: AsyncSession, **filter_by):
        """Удаляет записи, соответствующие фильтру."""
        try:
            query = delete(cls.model).filter_by(**filter_by)
            await session.execute(query)
            await session.commit()
        except IntegrityError as e:
            # Проверяем, является ли ошибка нарушением ограничения внешнего ключа
            if isinstance(e.orig, AsyncAdapt_asyncpg_dbapi.IntegrityError) and 'ForeignKeyViolationError' in str(
                    e.orig):
                logger.warning(
                    "Violation of the rules for using a foreign key, the value is referenced in another table")
                raise LinkM2MException
        return {"Запись успешно удалена"}
