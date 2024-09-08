from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from exceptions import OkStatusCode
from models.users import Users
from schemas.tags import TagSchema, TagShortSchema
from services.tag_service import TagService
from users.dependencies import get_current_user
from logger_config import logger

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
    logger.info("Fetching all tags")
    tags = await TagService.find_all(session)
    logger.info(f"Found {len(tags)} tags")
    return tags


@router.post("",
             response_model=TagShortSchema,
             description="This method creates a new tag",
             )
async def create_tag(
        tag: str,
        auth: bool = Depends(get_current_user),
        session: AsyncSession = Depends(get_db),
):
    logger.info(f"Creating new tag: {tag}")
    new_tag = await TagService.add(session, name=tag)
    logger.info(f"Tag: {tag} created successfully with ID {new_tag.id}")
    return new_tag


@router.get("/{tag_id}",
            response_model=TagShortSchema,
            description="This method returns the tag's details by id",
            )
async def get_tag_by_id(
        tag_id: int,
        auth: bool = Depends(get_current_user),
        session: AsyncSession = Depends(get_db),
):
    logger.info(f"Fetching tag by ID: {tag_id}")
    tag = await TagService.find_one_or_none(session, id=tag_id)
    logger.info(f"Tag found: {tag.name}")
    return tag


@router.put("/{tag_id}",
            response_model=TagShortSchema,
            description="This method updates the tag's details by id",
            )
async def update_tag(
        tag_id: int,
        name: str,
        auth: bool = Depends(get_current_user),
        session: AsyncSession = Depends(get_db),
):
    logger.info(f"Updating tag ID: {tag_id} with new name: {name}")
    updated_tag = await TagService.update(session, id=tag_id, name=name)
    logger.info(f"Tag ID: {tag_id} updated successfully")
    return updated_tag


@router.delete("/{tag_id}",
               description="This method deletes the tag's by id",
               )
async def delete_tag(
        tag_id: int,
        auth: bool = Depends(get_current_user),
        session: AsyncSession = Depends(get_db),
):
    logger.info(f"Deleting tag with ID: {tag_id}")
    await TagService.delete(session, id=tag_id)
    logger.info(f"Tag ID: {tag_id} deleted successfully")
    return OkStatusCode().detail
