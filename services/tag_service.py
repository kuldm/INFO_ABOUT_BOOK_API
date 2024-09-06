from sqlalchemy import select

from database import async_session_maker
from models.tags import Tag
from services.base import BaseService


class TagService(BaseService):
    model = Tag
