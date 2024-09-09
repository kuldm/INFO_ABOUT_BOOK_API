from datetime import datetime, timedelta
from http.client import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from jose import jwt
from passlib.context import CryptContext

from config import settings
from exceptions import UserIsNotPresentException
from services.user_service import UserService
from logger_config import logger


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, settings.ALGORITHM
    )
    return encoded_jwt


async def authenticate_user(username: str, password: str):
    user = await UserService.find_user(username=username)
    if not user:
        logger.info(f"User: {username} does not exist")
        raise UserIsNotPresentException
    if not verify_password(password, user.hashed_password):
        logger.info(f"Invalid password for user: {username}")
        raise UserIsNotPresentException
    return user
