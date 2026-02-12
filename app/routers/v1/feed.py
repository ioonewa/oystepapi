from fastapi import APIRouter, Query, Depends, HTTPException
from typing import List, Optional
from app.services.feed import FeedService
from app.database.unit_of_work import UnitOfWork
from app.models.feed import FeedItemPageDTO, FeedPageDTO, FeedItemTypeDTO
from app.dependencies.auth import get_current_user

from app.services.education import EducationService
from app.models.feed import LessonDetail

router = APIRouter(prefix="/feed", tags=["Feed"])

# --- Лента ---
@router.get("/", response_model=FeedPageDTO)
async def get_feed(
    cursor: Optional[str] = Query(None, description="ID последнего поста для пагинации"),
    limit: int = Query(20, description="Количество постов на страницу"),
    types: Optional[List[str]] = Query(None, description="Фильтр по типам постов"),
    include_favourites: bool = Query(False, description="Включить избранное"),
    q: Optional[str] = Query(None, description="Поиск по заголовку или описанию"),
    current_user=Depends(get_current_user)
):
    async with UnitOfWork() as uow:
        service = FeedService(uow)
        return await service.get_feed(
            cursor, limit, types, current_user.id, include_favourites, q
        )


@router.get("/types", response_model=List[FeedItemTypeDTO])
async def get_feed_types():
    """
    Список категорий постов (для фильтрации и UI)
    """
    async with UnitOfWork() as uow:
        service = FeedService(uow)
        return await service.get_feed_types()


# --- Добавить в избранное ---
@router.post("/favourites/{feed_item_id}")
async def add_favourite(
    feed_item_id: int,
    current_user=Depends(get_current_user)
):
    async with UnitOfWork() as uow:
        service = FeedService(uow)
        await service.add_favourite(current_user.id, feed_item_id)
    return {"status": "ok", "message": "Added to favourites"}

# --- Удалить из избранного ---
@router.delete("/favourites/{feed_item_id}")
async def remove_favourite(
    feed_item_id: int,
    current_user=Depends(get_current_user)
):
    async with UnitOfWork() as uow:
        service = FeedService(uow)
        await service.remove_favourite(current_user.id, feed_item_id)
    return {"status": "ok", "message": "Removed from favourites"}

@router.get(
    "/{feed_item_id}/lessons/{lesson_id}",
    response_model=LessonDetail,
    summary="Детали урока",
    description="Возвращает информацию об уроке, включая ссылки на видео, предыдущий и следующий урок"
)
async def get_lesson_details(feed_item_id: int, lesson_id: int):
    async with UnitOfWork() as uow:
        service = EducationService(uow)
        lesson = await service.get_lesson_detail(feed_item_id, lesson_id)
        if not lesson:
            raise HTTPException(status_code=404, detail="Lesson not found")
        return lesson

# --- Детали поста ---
@router.get("/{feed_item_id}", response_model=FeedItemPageDTO)
async def get_feed_item(
    feed_item_id: int,
    current_user=Depends(get_current_user)
):
    async with UnitOfWork() as uow:
        service = FeedService(uow)
        post = await service.get_feed_item_detail(feed_item_id, current_user.id)
        if not post:
            raise HTTPException(status_code=404, detail="Feed item not found")
        return post

