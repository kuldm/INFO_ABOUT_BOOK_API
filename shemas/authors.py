from typing import List, Optional

from pydantic import BaseModel


class SchemaAuthor(BaseModel):
    id: int
    name: str
    books: Optional[List[List]]
