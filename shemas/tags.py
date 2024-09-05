from typing import List, Optional

from pydantic import BaseModel


class SchemaTag(BaseModel):
    id: int
    name: str
    books: Optional[List[List]]
