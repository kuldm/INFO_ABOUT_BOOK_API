from typing import List

from fastapi import APIRouter, Depends

from schemas.authors import AuthorSchema, AuthorShortSchema
from services.author_service import AuthorService

router = APIRouter(
    prefix="/authors",
    tags=["Авторы"],
)


@router.get("",
            response_model=List[AuthorSchema],
            description="This method returns a list of all authors",
            )
async def get_authors():
    return await AuthorService.find_all()


@router.post("",
             response_model=AuthorShortSchema,
             description="This method creates a new author",
             )
async def create_author(
        author_name: str,
):
    return await AuthorService.add(name=author_name)


@router.get("/{author_id}",
            response_model=AuthorShortSchema,
            description="This method returns the author's by id",
            )
async def get_author_by_id(
        author_id: int,
):
    return await AuthorService.find_one_or_none(id=author_id)


@router.put("/{author_id}",
            response_model=AuthorSchema,
            description="This method updates the author's details by id",
            )
async def update_author(author_id):
    pass


@router.delete("/{author_id}",
               description="This method deletes the author's by id",
               )
async def delete_author(
        author_id: int,
):
    return await AuthorService.delete(id=author_id)
