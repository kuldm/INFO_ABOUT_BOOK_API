from sqlalchemy import select, insert, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.postgresql.asyncpg import AsyncAdapt_asyncpg_dbapi
from fastapi import Response

from exceptions import LinkM2MException, UserIsNotPresentException, UserAlreadyExistException, \
    UserSuccessfullyRegisteredCode, SuccessfulLoggingCode

from logger_config import logger
from services.base import BaseService
from services.user_service import UserService
from users.auth import get_password_hash, authenticate_user, create_access_token


class RegistrationAndLoginService(BaseService):
    model = None

    @classmethod
    async def register_user(cls, username: str, password: str):
        existing_user = await UserService.find_user(username=username)
        if existing_user:
            logger.warning(f"User {username} already exists")
            raise UserAlreadyExistException
        hashed_password = get_password_hash(password)
        await UserService.add_user(username=username, hashed_password=hashed_password)
        return UserSuccessfullyRegisteredCode().detail

    @classmethod
    async def login_user(cls, response: Response, username: str, password: str):
        user = await authenticate_user(username=username, password=password)
        if not user:
            logger.error(f"Failed login attempt for user: {username}")
            raise UserIsNotPresentException
        access_token = create_access_token({"sub": str(user.id)})
        response.set_cookie("user_access_token", access_token, httponly=True)
        return SuccessfulLoggingCode().detail
