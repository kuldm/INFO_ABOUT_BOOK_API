from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database import async_session_maker
from models.authors import Author
from services.base import BaseService


class AuthorService(BaseService):
    model = Author
