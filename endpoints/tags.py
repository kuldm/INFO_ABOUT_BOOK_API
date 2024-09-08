from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models.users import Users
from schemas.tags import TagSchema, TagShortSchema
from services.tag_service import TagService
from users.dependencies import get_current_user

router = APIRouter(
    prefix="/tags",
    tags=["Тэги"],
)


@router.get("",
            response_model=List[TagSchema],
            description="This method returns a list of all tags",
            )
async def get_tags(
        auth: bool = Depends(get_current_user),
        session: AsyncSession = Depends(get_db),
):
    return await TagService.find_all(session)


@router.post("",
             response_model=TagShortSchema,
             description="This method creates a new tag",
             )
async def create_tag(
        tag: str,
        auth: bool = Depends(get_current_user),
        session: AsyncSession = Depends(get_db),
):
    return await TagService.add(session, name=tag)


@router.get("/{tag_id}",
            response_model=TagShortSchema,
            description="This method returns the tag's details by id",
            )
async def get_tag_by_id(
        tag_id: int,
        auth: bool = Depends(get_current_user),
):
    return await TagService.find_one_or_none(id=tag_id)


@router.put("/{tag_id}",
            response_model=TagShortSchema,
            description="This method updates the tag's details by id",
            )
async def update_tag(
        tag_id: int,
        name: str,
        auth: bool = Depends(get_current_user),

):
    return await TagService.update(id=tag_id, name=name)


@router.delete("/{tag_id}",
               description="This method deletes the tag's by id",
               )
async def delete_tag(
        tag_id: int,
        auth: bool = Depends(get_current_user),

):
    return await TagService.delete(id=tag_id)
