from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from schemas.books import BookSchema, BookShortSchema
from services.book_service import BookService
from users.dependencies import get_current_user

router = APIRouter(
    prefix="/books",
    tags=["Книги"],
)


@router.get("",
            response_model=List[BookSchema],
            description="This method returns a list of all books",
            )
async def get_books(
        auth: bool = Depends(get_current_user),
        session: AsyncSession = Depends(get_db),

):
    return await BookService.find_all_books(session)


@router.post("",
             response_model=BookShortSchema,
             description="This method creates a new book",
             )
async def create_book(
        name: str,
        authors: List[str],
        tags: List[str],
        auth: bool = Depends(get_current_user),
        session: AsyncSession = Depends(get_db),

):
    return await BookService.add_book(session, name=name, authors=authors, tags=tags)


@router.get("/{book_id}",
            response_model=BookShortSchema,
            description="This method returns the book's by id",
            )
async def get_book_by_id(
        book_id: int,
        auth: bool = Depends(get_current_user),
        session: AsyncSession = Depends(get_db),

):
    return await BookService.find_one_or_none(session, id=book_id)


@router.put("/{book_id}",
            response_model=BookShortSchema,
            description="This method updates the book's details by id",
            )
async def update_book(
        book_id: int,
        book_name: str,
        auth: bool = Depends(get_current_user),
        session: AsyncSession = Depends(get_db),

):
    return await BookService.update_book(session, book_id=book_id, name=book_name)


@router.delete("/{book_id}",
               description="This method deletes the book's by id",
               )
async def delete_book(
        book_id: int,
        auth: bool = Depends(get_current_user),
        session: AsyncSession = Depends(get_db),

):
    return await BookService.delete_book(session, book_id=book_id)
