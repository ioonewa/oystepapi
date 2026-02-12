from fastapi import APIRouter, HTTPException
from typing import List

from app.models.link import Link
from app.database.unit_of_work import UnitOfWork

router = APIRouter(prefix="/links", tags=["links"])


@router.get(
    "/",
    response_model=List[Link],
    summary="Получить список ссылок",
    description=(
        "Возвращает список всех доступных ссылок относящихся к проекты.\n\n"
        "Ссылки используются для отображения блоков с чатами, каналами или ботами"
    ),
)
async def get_links():
    async with UnitOfWork() as uow:
        links = await uow.links.get_list()

    return links


@router.get(
    "/{link_id}",
    response_model=Link,
    summary="Получить ссылку по ID",
    description=(
        "Возвращает детальную информацию о ссылке по её идентификатору"
    )
)
async def get_link(link_id: int):
    async with UnitOfWork() as uow:
        link = await uow.links.get_by_id(link_id)

    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    return link