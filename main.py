import uvicorn
from fastapi import FastAPI

from endpoints.authors import router as authors_router
from endpoints.books import router as books_router
from endpoints.tags import router as tags_router
from endpoints.users import router as users_router
from config import settings

app = FastAPI()

app.include_router(users_router)
app.include_router(authors_router)
app.include_router(books_router)
app.include_router(tags_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT)
