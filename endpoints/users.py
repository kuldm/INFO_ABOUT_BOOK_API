from fastapi import APIRouter, Response

from exceptions import UserIsNotPresentException, UserAlreadyExistException, OkStatusCode, \
    UserSuccessfullyRegisteredCode, UserLoggedOutCode, SuccessfulLoggingCode
from schemas.users import UserAuthSchema
from services.user_service import UserService
from users.auth import get_password_hash, authenticate_user, create_access_token
from logger_config import logger

router = APIRouter(
    prefix="/auth",
    tags=["Авторизация и пользователи"],
)


@router.post("/register",
             description="Этот метод создаёт нового пользователя"
             )
async def register_user(user_data: UserAuthSchema):
    logger.info(f"Registering user: {user_data.username}")
    existing_user = await UserService.find_user(username=user_data.username)
    if existing_user:
        logger.warning(f"User {user_data.username} already exists")
        raise UserAlreadyExistException
    hashed_password = get_password_hash(user_data.password)
    await UserService.add_user(username=user_data.username, hashed_password=hashed_password)
    logger.info(f"User {user_data.username} registered successfully")
    return UserSuccessfullyRegisteredCode().detail


@router.post("/login",
             description="Этот метод залогинивает пользователя",
             )
async def login_user(response: Response, user_data: UserAuthSchema):
    logger.info(f"Logging in user: {user_data.username}")
    user = await authenticate_user(username=user_data.username, password=user_data.password)
    if not user:
        logger.error(f"Failed login attempt for user: {user_data.username}")
        raise UserIsNotPresentException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("user_access_token", access_token, httponly=True)
    logger.info(f"User {user_data.username} logged in successfully")
    return SuccessfulLoggingCode().detail


@router.post("/logout",
             description="Этот метод разлогинивает пользователя"
             )
async def logout_user(response: Response):
    logger.info("Logging out user")
    response.delete_cookie("user_access_token")
    logger.info("User logged out successfully")
    return UserLoggedOutCode().detail


@router.delete("/{username}",
               description="Этот метод удаляет пользователя по его имени",
               )
async def delete_tag(
        username: str,
):
    logger.info(f"Deleting user: {username}")
    await UserService.delete_user(username=username)
    logger.info(f"User {username} deleted successfully")
    return OkStatusCode().detail
