from typing import List, Optional

from pydantic import BaseModel


class BookShortSсhema(BaseModel):
    id: int
    title: str

    class Config:
        from_attributes = True


class AuthorSchema(BaseModel):
    id: int
    name: str
    books: Optional[List[BookShortSсhema]]

    class Config:
        from_attributes = True


class AuthorShortSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

