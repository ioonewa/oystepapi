from typing import List
from app.services.mappers import map_geojson_point
from app.models.selection import SelectionMapItem, FeedItemCardDTO
from app.database.unit_of_work import UnitOfWork
from app.models.feed import MediaItemDTO

class SelectionService:
    uow: UnitOfWork

    def __init__(self, uow: UnitOfWork):
        self.uow=uow

    async def get_map_items(
        self,
        min_lon: float,
        min_lat: float,
        max_lon: float,
        max_lat: float
    ) -> List[SelectionMapItem]:

        # получаем все свойства + связанные feed_item_id
        rows = await self.uow.selections.get_properties_in_bbox(
            min_lon=min_lon,
            min_lat=min_lat,
            max_lon=max_lon,
            max_lat=max_lat
        )

        if not rows:
            return []

        # собираем все preview_media_id для batch
        media_ids = {row["preview_media_id"] for row in rows if row["preview_media_id"]}
        media_map = await self.uow.feed.get_media_by_ids(media_ids)

        # группируем свойства по feed_item_id (каждая карточка одна)
        feed_map: dict[int, dict] = {}

        for row in rows:
            fid = row["feed_id"]
            if fid not in feed_map:
                feed_map[fid] = {
                    "feed_id": fid,
                    "title": row["title"],
                    "short_description": row["short_description"],
                    "preview_media_id": row["preview_media_id"],
                    "published_at": row["published_at"],
                    "properties": []
                }

            feed_map[fid]["properties"].append({
                "id": row["property_id"],
                "name": row["property_name"],
                "latitude": row["latitude"],
                "longitude": row["longitude"],
            })

        # формируем SelectionMapItem с FeedItemCardDTO + media
        result: List[SelectionMapItem] = []

        for feed in feed_map.values():
            # получаем media для карточки
            media: List[MediaItemDTO] = []
            if feed["preview_media_id"] and feed["preview_media_id"] in media_map:
                media.append(MediaItemDTO(**media_map[feed["preview_media_id"]]))

            item = FeedItemCardDTO(
                id=feed["feed_id"],
                type="selection",
                title=feed["title"],
                short_description=feed["short_description"],
                published_at=feed['published_at'],
                preview_media_id=feed["preview_media_id"],
                media=media,
                is_favourite=False # ToDo Заглушка
            )

            for prop in feed["properties"]:
                result.append(
                    SelectionMapItem(
                        location=map_geojson_point({
                            "type": "Point",
                            "coordinates": [prop["longitude"], prop["latitude"]]
                        }),
                        item=item
                    )
                )

        return result
