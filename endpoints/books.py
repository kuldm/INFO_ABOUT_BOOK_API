from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from exceptions.exceptions import OkStatusCode
from schemas.books import BookSchema, BookShortSchema
from services.book_service import BookService
from users.dependencies import get_current_user
from utils.wrapers import log_request

router = APIRouter(
    prefix="/books",
    tags=["Книги"],
    dependencies=[Depends(get_current_user)],
)


@router.get("",
            response_model=List[BookSchema],
            description="Этот метод возвращает данные всех книг, либо данные книг по заданным параметрам",
            )
@log_request
async def get_books(
        session: AsyncSession = Depends(get_db),
        author_id: Optional[int] = Query(None),
        tag_id: Optional[int] = None,
):
    return await BookService.find_all_books(session, author_id, tag_id)


@router.post("",
             response_model=BookShortSchema,
             description="Этот метод создаёт новую книгу",
             )
@log_request
async def create_book(
        name: str,
        authors: List[str],
        tags: List[str],
        session: AsyncSession = Depends(get_db),

):
    return await BookService.add_book(session, name=name, authors=authors, tags=tags)


@router.get("/{book_id}",
            response_model=BookSchema,
            description="Этот метод возвращает данные книги по её ID",
            )
@log_request
async def get_book_by_id(
        book_id: int,
        session: AsyncSession = Depends(get_db),

):
    return await BookService.find_one_or_none_book(session, id=book_id)


@router.put("/{book_id}",
            response_model=BookShortSchema,
            description="Этот метод обновляет данные книги по её ID",
            )
@log_request
async def update_book(
        book_id: int,
        book_name: str,
        session: AsyncSession = Depends(get_db),

):
    return await BookService.update_book(session, book_id=book_id, name=book_name)


@router.delete("/{book_id}",
               description="Этот метод удаляет книгу по его ID",
               )
@log_request
async def delete_book(
        book_id: int,
        session: AsyncSession = Depends(get_db),

):
    await BookService.delete_book(session, book_id=book_id)
    return OkStatusCode().detail
