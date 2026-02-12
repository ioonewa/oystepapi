from app.models.feed import (
    FeedItemCardDTO,
    FeedItemPageDTO,

    FeedItemTypeDTO,
    
    MediaItemDTO,
    ButtonDTO,
    PropertyDTO,
    SelectionContentDTO,
    FeedPageDTO
)
from app.database.unit_of_work import UnitOfWork
from typing import List, Optional

import base64
import json


class FeedService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
    # ------------------------
    # ЛЕНТА (CARD)
    # ------------------------
    async def get_feed(
        self,
        cursor: Optional[str] = None,
        limit: int = 20,
        types: Optional[List[str]] = None,
        user_id: Optional[int] = None,
        include_favourites: bool = False,
        q: Optional[str] = None
    ) -> FeedPageDTO:

        rows = await self.uow.feed.get_feed_items(
            cursor, limit, types, user_id, include_favourites, q
        )

        media_map = await self.uow.feed.get_media_by_ids(
            row["preview_media_id"] for row in rows
        )

        feed: list[FeedItemCardDTO] = []

        for row in rows:
            media = []
            if row["preview_media_id"]:
                media.append(MediaItemDTO(**media_map[row["preview_media_id"]]))

            feed.append(
                FeedItemCardDTO(
                    id=row["id"],
                    type=row["type"],
                    published_at=row["published_at"],
                    title=row["title"],
                    short_description=row.get("short_description"),
                    preview_media_id=row["preview_media_id"],
                    media=media,
                    is_favourite=row["is_favourite"]
                )
            )

        # --- формируем следующий курсор ---
        next_cursor = None
        if feed:
            last = feed[-1]
            cursor_obj = {
                "id": last.id,
                "published_at": last.published_at.isoformat()
            }
            next_cursor = base64.b64encode(json.dumps(cursor_obj).encode()).decode()

        return {
            "items": feed,
            "next_cursor": next_cursor
        }


    # ------------------------
    # ДЕТАЛЬНАЯ СТРАНИЦА (PAGE)
    # ------------------------
    async def get_feed_item_detail(
        self, feed_item_id: int, user_id: int
    ) -> Optional[FeedItemPageDTO]:

        row = await self.uow.feed.get_feed_item_detail(feed_item_id, user_id)
        if not row:
            return None

        # --- media ---
        media = [MediaItemDTO(**m) for m in row.get("media", [])]

        # --- button ---
        button = None
        if row.get("button_text") and row.get("button_link"):
            button = ButtonDTO(
                text=row["button_text"],
                link=row["button_link"],
            )

        # --- selection ---
        selection = None
        if row["type"] == "selection":
            selection_type = row.get("selection_type")

            # properties: ТОЛЬКО для single
            properties = []
            if selection_type == "single":
                properties = [
                    PropertyDTO(
                        id=p["id"],
                        name=p["name"],
                        latitude=p["latitude"],
                        longitude=p["longitude"],
                        address=p.get("address"),
                        city=p.get("city"),
                    )
                    for p in row.get("properties", [])
                ]

            # related selections → карточки
            related_cards: list[FeedItemCardDTO] = []
            related = row.get("related_selections", [])

            # получаем media только для связанных подборок
            media_map = await self.uow.feed.get_media_by_ids(
                r["preview_media_id"] for r in related if r.get("preview_media_id")
            )

            for r in related:
                related_media: list[MediaItemDTO] = []

                preview_id = r.get("preview_media_id")
                if preview_id and preview_id in media_map:
                    related_media.append(MediaItemDTO(**media_map[preview_id]))

                related_cards.append(
                    FeedItemCardDTO(
                        id=r["id"],
                        type="selection",
                        published_at=r["published_at"],
                        title=r["title"],
                        short_description=r.get("short_description"),
                        preview_media_id=preview_id,
                        media=related_media,
                        is_favourite=r.get("is_favourite", False)
                    )
                )

            selection = SelectionContentDTO(
                selection_type=selection_type,
                properties=properties,
                related_selections=related_cards,
            )

        # --- card base ---
        card = FeedItemCardDTO(
            id=row["id"],
            type=row["type"],
            published_at=row["published_at"],
            title=row["title"],
            short_description=row.get("short_description"),
            preview_media_id=row["preview_media_id"],
            media=media,
            is_favourite=row["is_favourite"]  
        )

        # --- page ---
        return FeedItemPageDTO(
            **card.model_dump(),
            body=row.get("body"),
            button=button,
            selection=selection,
        )

    async def get_feed_types(self) -> list[FeedItemTypeDTO]:
        rows = await self.uow.feed.get_feed_item_types()
        return [FeedItemTypeDTO(**row) for row in rows]
    
    # --- Добавить в избранное ---
    async def add_favourite(self, user_id: int, feed_item_id: int):
        await self.uow.user_favourites.add_favourite(user_id, feed_item_id)

    # --- Удалить из избранного ---
    async def remove_favourite(self, user_id: int, feed_item_id: int):
        await self.uow.user_favourites.remove_favourite(user_id, feed_item_id)