from typing import List

from fastapi import APIRouter

from schemas.tags import TagSchema, TagShortSchema
from services.tag_service import TagService

router = APIRouter(
    prefix="/tags",
    tags=["Тэги"],
)


@router.get("",
            response_model=List[TagSchema],
            description="This method returns a list of all tags",
            )
async def get_tags():
    return await TagService.find_all()


@router.post("",
             response_model=TagSchema,
             description="This method creates a new tag",
             )
async def create_tag():
    pass


@router.get("/{tag_id}",
            response_model=TagShortSchema,
            description="This method returns the tag's details by id",
            )
async def get_tag_by_id(
        tag_id: int,
):
    return await TagService.find_one_or_none(id=tag_id)


@router.put("/{tag_id}",
            response_model=TagSchema,
            description="This method updates the tag's details by id",
            )
async def update_tag(tag_id):
    pass


@router.delete("/{tag_id}",
               description="This method deletes the tag's by id",
               )
async def delete_tag(tag_id):
    pass
