from typing import List

from fastapi import APIRouter

from shemas.books import SchemaBook

router = APIRouter(
    prefix="/books",
    tags=["Книги"],
)


@router.get("",
            description="This method returns a list of all books",
            )
async def get_books():
    books = "Книги"
    return books


@router.post("",
             description="This method creates a new book",
             )
async def create_book():
    pass


@router.get("/{book_id}",
            description="This method returns the book's details by id",
            )
async def get_book(book_id):
    pass


@router.put("/{book_id}",
            description="This method updates the book's details by id",
            )
async def update_book(book_id):
    pass


@router.delete("/{book_id}",
               description="This method deletes the book's by id",
               )
async def delete_book(book_id):
    pass
