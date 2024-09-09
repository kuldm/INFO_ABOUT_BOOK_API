from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from exceptions import OkStatusCode
from schemas.authors import AuthorSchema, AuthorShortSchema
from services.author_service import AuthorService
from users.dependencies import get_current_user
from logger_config import logger

router = APIRouter(
    prefix="/authors",
    tags=["Авторы"],
)


@router.get("",
            response_model=List[AuthorSchema],
            description="Этот метод возвращает данные всех авторов",
            )
async def get_authors(
        auth: bool = Depends(get_current_user),
        session: AsyncSession = Depends(get_db),
):
    logger.info("Fetching all authors")
    authors = await AuthorService.find_all(session)
    logger.info(f"Found {len(authors)} authors")
    return authors


@router.post("",
             response_model=AuthorShortSchema,
             description="Этот метод создаёт нового автора",
             )
async def create_author(
        author_name: str,
        auth: bool = Depends(get_current_user),
        session: AsyncSession = Depends(get_db),

):
    logger.info(f"Creating new author: {author_name}")
    new_author = await AuthorService.add(session, name=author_name)
    logger.info(f"Author: {author_name} created successfully with ID: {new_author.id}")
    return new_author


@router.get("/{author_id}",
            response_model=AuthorShortSchema,
            description="Этот метод возвращает данные автора по его ID",
            )
async def get_author_by_id(
        author_id: int,
        auth: bool = Depends(get_current_user),
        session: AsyncSession = Depends(get_db),

):
    logger.info(f"Fetching author by ID: {author_id}")
    author = await AuthorService.find_one_or_none(session, id=author_id)
    logger.info(f"Author found: {author.name}")
    return author


@router.put("/{author_id}",
            response_model=AuthorShortSchema,
            description="Этот метод обновляет данные автора по его ID",
            )
async def update_author(
        author_id: int,
        author_name: str,
        auth: bool = Depends(get_current_user),
        session: AsyncSession = Depends(get_db),

):
    logger.info(f"Updating author ID: {author_id} with new name: {author_name}")
    updated_author = await AuthorService.update(session, id=author_id, name=author_name)
    logger.info(f"Author ID: {author_id} updated successfully")
    return updated_author


@router.delete("/{author_id}",
               description="Этот метод удаляет автора по его ID",
               )
async def delete_author(
        author_id: int,
        auth: bool = Depends(get_current_user),
        session: AsyncSession = Depends(get_db),

):
    logger.info(f"Deleting author with ID: {author_id}")
    await AuthorService.delete(session, id=author_id)
    logger.info(f"Author ID: {author_id} deleted successfully")
    return OkStatusCode().detail
