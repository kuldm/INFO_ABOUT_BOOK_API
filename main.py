import uvicorn
from fastapi import FastAPI
import logging

from logger_config import logger

from config import settings

from endpoints.authors import router as authors_router
from endpoints.books import router as books_router
from endpoints.tags import router as tags_router
from endpoints.users import router as users_router

app = FastAPI(
    title="Book API",
    description="Приложение для управления книгами, авторами, тегами и пользователями",
    version="1.0.0"
)

app.include_router(users_router)
app.include_router(authors_router)
app.include_router(books_router)
app.include_router(tags_router)

if __name__ == "__main__":
    logger.info("--- Starting up application ---")
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT)
