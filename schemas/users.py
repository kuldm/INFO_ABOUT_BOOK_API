from pydantic import BaseModel


class UserAuthSchema(BaseModel):
    name: str
    password: str
