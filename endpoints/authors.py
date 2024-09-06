from typing import List

from fastapi import APIRouter, Depends

from schemas.authors import AuthorSchema
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
             response_model=AuthorSchema,
             description="This method creates a new author",
             )
async def create_author():
    pass


@router.get("/{author_id}",
            response_model=AuthorSchema,
            description="This method returns the author's details by id",
            )
async def get_author(author_id):
    pass


@router.put("/{author_id}",
            response_model=AuthorSchema,
            description="This method updates the author's details by id",
            )
async def update_author(author_id):
    pass


@router.delete("/{author_id}",
               description="This method deletes the author's by id",
               )
async def delete_author(author_id):
    pass
