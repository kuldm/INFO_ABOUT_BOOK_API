from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from exceptions import OkStatusCode
from schemas.books import BookSchema, BookShortSchema
from services.book_service import BookService
from users.dependencies import get_current_user
from logger_config import logger

router = APIRouter(
    prefix="/books",
    tags=["Книги"],
)


@router.get("",
            response_model=List[BookSchema],
            description="Этот метод возвращает данные всех книг, либо данные книг по заданным параметрам",
            )
async def get_books(
        auth: bool = Depends(get_current_user),
        session: AsyncSession = Depends(get_db),
        author_id: Optional[int] = Query(None),
        tag_id: Optional[int] = None,
):
    logger.info(f"Fetching books with author_id={author_id} and tag_id={tag_id}")
    books = await BookService.find_all_books(session, author_id, tag_id)
    logger.info(f"Found {len(books)} books")
    return books


@router.post("",
             response_model=BookShortSchema,
             description="Этот метод создаёт новую книгу",
             )
async def create_book(
        name: str,
        authors: List[str],
        tags: List[str],
        auth: bool = Depends(get_current_user),
        session: AsyncSession = Depends(get_db),

):
    logger.info(f"Creating new book: {name}, authors: {authors}, tags: {tags}")
    new_book = await BookService.add_book(session, name=name, authors=authors, tags=tags)
    logger.info(f"Book: {name} created successfully")
    return new_book


@router.get("/{book_id}",
            response_model=BookSchema,
            description="Этот метод возвращает данные книги по её ID",
            )
async def get_book_by_id(
        book_id: int,
        auth: bool = Depends(get_current_user),
        session: AsyncSession = Depends(get_db),

):
    logger.info(f"Fetching book by ID: {book_id}")
    book = await BookService.find_one_or_none_book(session, id=book_id)
    logger.info(f"Book found: {book.name}")
    return book


@router.put("/{book_id}",
            response_model=BookShortSchema,
            description="Этот метод обновляет данные книги по её ID",
            )
async def update_book(
        book_id: int,
        book_name: str,
        auth: bool = Depends(get_current_user),
        session: AsyncSession = Depends(get_db),

):
    logger.info(f"Updating book ID: {book_id} with new name: {book_name}")
    updated_book = await BookService.update_book(session, book_id=book_id, name=book_name)
    logger.info(f"Book ID: {book_id} updated successfully")
    return updated_book


@router.delete("/{book_id}",
               description="Этот метод удаляет книгу по его ID",
               )
async def delete_book(
        book_id: int,
        auth: bool = Depends(get_current_user),
        session: AsyncSession = Depends(get_db),

):
    logger.info(f"Deleting book with ID: {book_id}")
    await BookService.delete_book(session, book_id=book_id)
    logger.info(f"Book ID: {book_id} deleted successfully")
    return OkStatusCode().detail
