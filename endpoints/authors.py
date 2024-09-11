from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from exceptions.exceptions import OkStatusCode
from schemas.authors import AuthorSchema, AuthorShortSchema
from services.author_service import AuthorService
from users.dependencies import get_current_user
from utils.wrapers import log_request

router = APIRouter(
    prefix="/authors",
    tags=["Авторы"],
    dependencies=[Depends(get_current_user)],
)


@router.get("",
            response_model=List[AuthorSchema],
            description="Этот метод возвращает данные всех авторов",
            )
@log_request
async def get_authors(
        session: AsyncSession = Depends(get_db),
):
    return await AuthorService.find_all(session)


@router.post("",
             response_model=AuthorShortSchema,
             description="Этот метод создаёт нового автора",
             )
@log_request
async def create_author(
        author_name: str,
        session: AsyncSession = Depends(get_db),

):
    return await AuthorService.add(session, name=author_name)


@router.get("/{author_id}",
            response_model=AuthorShortSchema,
            description="Этот метод возвращает данные автора по его ID",
            )
@log_request
async def get_author_by_id(
        author_id: int,
        session: AsyncSession = Depends(get_db),

):
    return await AuthorService.find_one_or_none(session, id=author_id)


@router.put("/{author_id}",
            response_model=AuthorShortSchema,
            description="Этот метод обновляет данные автора по его ID",
            )
@log_request
async def update_author(
        author_id: int,
        author_name: str,
        session: AsyncSession = Depends(get_db),

):
    return await AuthorService.update(session, id=author_id, name=author_name)


@router.delete("/{author_id}",
               description="Этот метод удаляет автора по его ID",
               )
@log_request
async def delete_author(
        author_id: int,
        session: AsyncSession = Depends(get_db),

):
    await AuthorService.delete(session, id=author_id)
    return OkStatusCode().detail
