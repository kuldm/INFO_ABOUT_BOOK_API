from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from schemas.authors import AuthorSchema, AuthorShortSchema
from services.author_service import AuthorService
from users.dependencies import get_current_user

router = APIRouter(
    prefix="/authors",
    tags=["Авторы"],
)


@router.get("",
            response_model=List[AuthorSchema],
            description="This method returns a list of all authors",
            )
async def get_authors(
        auth: bool = Depends(get_current_user),
        session: AsyncSession = Depends(get_db),
):
    return await AuthorService.find_all(session)


@router.post("",
             response_model=AuthorShortSchema,
             description="This method creates a new author",
             )
async def create_author(
        author_name: str,
        auth: bool = Depends(get_current_user),
        session: AsyncSession = Depends(get_db),

):
    return await AuthorService.add(session, name=author_name)


@router.get("/{author_id}",
            response_model=AuthorShortSchema,
            description="This method returns the author's by id",
            )
async def get_author_by_id(
        author_id: int,
        auth: bool = Depends(get_current_user),
        session: AsyncSession = Depends(get_db),

):
    return await AuthorService.find_one_or_none(session, id=author_id)


@router.put("/{author_id}",
            response_model=AuthorShortSchema,
            description="This method updates the author's details by id",
            )
async def update_author(
        author_id: int,
        author_name: str,
        auth: bool = Depends(get_current_user),
        session: AsyncSession = Depends(get_db),

):
    return await AuthorService.update(session, id=author_id, name=author_name)


@router.delete("/{author_id}",
               description="This method deletes the author's by id",
               )
async def delete_author(
        author_id: int,
        auth: bool = Depends(get_current_user),
        session: AsyncSession = Depends(get_db),

):
    return await AuthorService.delete(session, id=author_id)
