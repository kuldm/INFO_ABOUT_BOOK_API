from http.client import HTTPException

from fastapi import APIRouter, Response
from sqlalchemy.testing.pickleable import User

from exceptions import UserIsNotPresentException, UserAlreadyExistException
from schemas.users import UserAuthSchema
from services.user_service import UserService
from users.auth import get_password_hash, verify_password, authenticate_user, create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Авторизация и пользователи"],
)


@router.post("/register",
             description="This method registers a new user"
             )
async def register_user(user_data: UserAuthSchema):
    existing_user = await UserService.find_one_or_none(name=user_data.name)
    if existing_user:
        raise UserAlreadyExistException
    hashed_password = get_password_hash(user_data.password)
    await UserService.add(name=user_data.name, hashed_password=hashed_password)


@router.post("/login",
             description="This method logining the user's",
             )
async def login_user(response: Response, user_data: UserAuthSchema):
    user = await authenticate_user(user_data.name, user_data.password)
    if not user:
        raise UserIsNotPresentException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("user_access_token", access_token, httponly=True)
    return {"access_token": access_token}


@router.post("/logout",
             description="This method logs out the user's"
             )
async def logout_user(response: Response):
    response.delete_cookie("user_access_token")


@router.delete("/{user_name}",
               description="This method deletes the user's by name",
               )
async def delete_tag(
        name: str,
):
    return await UserService.delete(name=name)
