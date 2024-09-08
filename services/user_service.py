from models.users import Users
from services.base import BaseService


class UserService(BaseService):
    model = Users
