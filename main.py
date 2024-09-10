import uvicorn
from fastapi import FastAPI
from utils.elasticsearch_utils import es_client

from endpoints.authors import router as authors_router
from endpoints.books import router as books_router
from endpoints.tags import router as tags_router
from endpoints.users import router as users_router

from config import settings
from logger_config import logger

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    # Проверяем подключение к Elasticsearch
    if not es_client.ping():
        raise ValueError("Не удалось подключиться к Elasticsearch")


app.include_router(users_router)
app.include_router(authors_router)
app.include_router(books_router)
app.include_router(tags_router)

if __name__ == "__main__":
    logger.info("Starting application...")
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT)
