from fastapi import Response

from exceptions import UserIsNotPresentException, UserAlreadyExistException, UserSuccessfullyRegisteredCode, \
    SuccessfulLoggingCode

from logger_config import logger
from services.base import BaseService
from services.user_service import UserService
from users.auth import get_password_hash, authenticate_user, create_access_token


class RegistrationAndLoginService(BaseService):
    model = None

    @classmethod
    async def register_user(cls, username: str, password: str):
        """Регистрация нового пользователя."""
        # Проверка на существование пользователя
        existing_user = await UserService.find_user(username=username)
        if existing_user:
            logger.warning(f"User {username} already exists")
            raise UserAlreadyExistException

        # Хэширование пароля и регистрация
        hashed_password = get_password_hash(password)
        await UserService.add_user(username=username, hashed_password=hashed_password)
        return UserSuccessfullyRegisteredCode().detail

    @classmethod
    async def login_user(cls, response: Response, username: str, password: str):
        """Аутентификация пользователя и установка куки с токеном."""
        # Аутентификация пользователя
        user = await authenticate_user(username=username, password=password)
        if not user:
            logger.error(f"Failed login attempt for user: {username}")
            raise UserIsNotPresentException

        # Создание JWT токена
        access_token = create_access_token({"sub": str(user.id)})

        # Установка куки с токеном
        response.set_cookie("user_access_token", access_token, httponly=True)
        return SuccessfulLoggingCode().detail
