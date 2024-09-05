from typing import List, Optional

from pydantic import BaseModel


class SchemaBook(BaseModel):
    id: int
    title: str
    authors: Optional[List[List]]
    tags: Optional[List[List]]
