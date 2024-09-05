from fastapi import APIRouter

router = APIRouter(
    prefix="/authors",
    tags=["Авторы"],
)


@router.get("",
            description="This method returns a list of all authors",
            )
async def get_authors():
    authors = "Авторы"
    return authors


@router.post("",
             description="This method creates a new author",
             )
async def create_author():
    pass


@router.get("/{author_id}",
            description="This method returns the author's details by id",
            )
async def get_author(author_id):
    pass


@router.put("/{author_id}",
            description="This method updates the author's details by id",
            )
async def update_author(author_id):
    pass


@router.delete("/{author_id}",
               description="This method deletes the author's by id",
               )
async def delete_author(author_id):
    pass
