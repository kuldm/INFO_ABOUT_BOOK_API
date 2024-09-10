from pydantic import BaseModel, SecretStr


class UserAuthSchema(BaseModel):
    username: str
    password: SecretStr
