from typing import List

from fastapi import APIRouter

from schemas.books import BookSchema, BookShortSchema
from services.book_service import BookService

router = APIRouter(
    prefix="/books",
    tags=["Книги"],
)


@router.get("",
            response_model=List[BookSchema],
            description="This method returns a list of all books",
            )
async def get_books():
    return await BookService.find_all_books()


@router.post("",
             response_model=BookSchema,
             description="This method creates a new book",
             )
async def create_book():
    pass


@router.get("/{book_id}",
            response_model=BookShortSchema,
            description="This method returns the book's by id",
            )
async def get_book_by_id(
        book_id: int,
):
    return await BookService.find_one_or_none(id=book_id)


@router.put("/{book_id}",
            response_model=BookShortSchema,
            description="This method updates the book's details by id",
            )
async def update_book(
        book_id: int,
        book_name: str
):
    return await BookService.update(id=book_id, name=book_name)


@router.delete("/{book_id}",
               description="This method deletes the book's by id",
               )
async def delete_book(
        book_id: int,
):
    return await BookService.delete(id=book_id)
