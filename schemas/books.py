from typing import List, Optional

from pydantic import BaseModel


class AuthorShortSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class TagShortSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class BookSchema(BaseModel):
    id: int
    title: str
    authors: Optional[List[AuthorShortSchema]]
    tags: Optional[List[TagShortSchema]]

    class Config:
        from_attributes = True


class BookShortSchema(BaseModel):
    id: int
    title: str

    class Config:
        from_attributes = True
