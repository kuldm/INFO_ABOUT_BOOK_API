from fastapi import APIRouter, Response

from exceptions import OkStatusCode, UserLoggedOutCode
from schemas.users import UserAuthSchema
from services.registration_and_logging_service import RegistrationAndLoginService
from services.user_service import UserService
from utils.wrapers import log_users_request

router = APIRouter(
    prefix="/auth",
    tags=["Авторизация и пользователи"],
)


@router.post("/register",
             description="Этот метод создаёт нового пользователя"
             )
@log_users_request
async def register_user(user_data: UserAuthSchema):
    return await RegistrationAndLoginService.register_user(username=user_data.username, password=user_data.password)


@router.post("/login",
             description="Этот метод залогинивает пользователя",
             )
@log_users_request
async def login_user(response: Response, user_data: UserAuthSchema):
    return await RegistrationAndLoginService.login_user(
        response, username=user_data.username, password=user_data.password)


@router.post("/logout",
             description="Этот метод разлогинивает пользователя"
             )
@log_users_request
async def logout_user(response: Response):
    response.delete_cookie("user_access_token")
    return UserLoggedOutCode().detail


@router.delete("/{username}",
               description="Этот метод удаляет пользователя по его имени",
               )
@log_users_request
async def delete_user(
        username: str,
):
    await UserService.delete_user(username=username)
    return OkStatusCode().detail
