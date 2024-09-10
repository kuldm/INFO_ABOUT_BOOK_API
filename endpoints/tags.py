from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from exceptions import OkStatusCode
from schemas.tags import TagSchema, TagShortSchema
from services.tag_service import TagService
from users.dependencies import get_current_user
from utils.wrapers import log_request

router = APIRouter(
    prefix="/tags",
    tags=["Тэги"],
    dependencies=[Depends(get_current_user)],
)


@router.get("",
            response_model=List[TagSchema],
            description="Этот метод возвращает данные всех тэгов",
            )
@log_request
async def get_tags(
        session: AsyncSession = Depends(get_db),
):
    return await TagService.find_all(session)


@router.post("",
             response_model=TagShortSchema,
             description="Этот метод создаёт новый тэг",
             )
@log_request
async def create_tag(
        tag: str,
        session: AsyncSession = Depends(get_db),
):
    return await TagService.add(session, name=tag)


@router.get("/{tag_id}",
            response_model=TagShortSchema,
            description="Этот метод возвращает данные тэга по его ID",
            )
@log_request
async def get_tag_by_id(
        tag_id: int,
        session: AsyncSession = Depends(get_db),
):
    return await TagService.find_one_or_none(session, id=tag_id)


@router.put("/{tag_id}",
            response_model=TagShortSchema,
            description="Этот метод обновляет данные тэга по его ID",
            )
@log_request
async def update_tag(
        tag_id: int,
        name: str,
        session: AsyncSession = Depends(get_db),
):
    return await TagService.update(session, id=tag_id, name=name)


@router.delete("/{tag_id}",
               description="Этот метод удаляет тэг по его ID",
               )
@log_request
async def delete_tag(
        tag_id: int,
        session: AsyncSession = Depends(get_db),
):
    await TagService.delete(session, id=tag_id)
    return OkStatusCode().detail
