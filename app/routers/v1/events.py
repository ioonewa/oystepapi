from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List
from datetime import datetime

from app.models.event import EventSummary, EventDetail
from app.database.unit_of_work import UnitOfWork

router = APIRouter(prefix="/events", tags=["events"])

@router.get(
    "/",
    response_model=List[EventSummary],
    summary="Список мероприятий",
    description=(
        "Возвращает список мероприятий с постраничной навигацией по cursor-based pagination. "
        "Сортировка выполняется по дате проведения (`event_at`) и `id`."
    )
)
async def get_events(
    limit: int = Query(20, ge=1, le=100),
    cursor_event_at: Optional[datetime] = Query(
        None, description="event_at последнего элемента"
    ),
    cursor_id: Optional[int] = Query(
        None, description="id последнего элемента"
    ),
):
    async with UnitOfWork() as uow:
        events = await uow.events.get_list(
            limit=limit,
            cursor_event_at=cursor_event_at,
            cursor_id=cursor_id,
        )

    return events

@router.get(
    "/search",
    response_model=List[EventSummary],
    summary="Поиск мероприятий",
    description="Prefix-поиск по названию, спикеру, адресу и описанию. Cursor-based pagination."
)
async def search_events(
    q: str = Query(..., min_length=1, description="Поисковая строка (с первых букв)"),
    limit: int = Query(20, ge=1, le=100),
    cursor_event_at: Optional[datetime] = Query(None, description="event_at последнего элемента"),
    cursor_id: Optional[int] = Query(None, description="id последнего элемента"),
):
    async with UnitOfWork() as uow:
        events = await uow.events.search(
            q=q,
            limit=limit,
            cursor_event_at=cursor_event_at,
            cursor_id=cursor_id,
        )
    return events

@router.get(
    "/{event_id}",
    response_model=EventDetail,
    summary="Детали мероприятия",
    description=(
        "Возвращает детальную информацию о мероприятии по его идентификатору. "
        "Если мероприятие не найдено — возвращается ошибка 404."
    )
)
async def event_details(event_id: int):
    async with UnitOfWork() as uow:
        event = await uow.events.get_by_id(event_id)

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    return event

