import uvicorn
from fastapi import FastAPI

from endpoints.authors import router as authors_router
from endpoints.books import router as books_router
from endpoints.tags import router as tags_router

app = FastAPI()

app.include_router(authors_router)
app.include_router(books_router)
app.include_router(tags_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
