from typing import List
from ..base import BaseRepository

class SelectionRepository(BaseRepository):
    
    async def get_properties_in_bbox(
        self,
        min_lon: float,
        min_lat: float,
        max_lon: float,
        max_lat: float
    ) -> List[dict]:
        """
        Возвращает список всех объектов и связанных карточек Selection типа 'single',
        попадающих в bbox
        """
        return await self.fetch("""
            SELECT 
                sp.feed_item_id,
                f.id AS feed_id,
                f.type,
                f.published_at,
                c.title,
                c.short_description,
                c.preview_media_id,
                p.id AS property_id,
                p.name AS property_name,
                ST_X(p.location::geometry) AS longitude,
                ST_Y(p.location::geometry) AS latitude
            FROM selection_properties sp
            JOIN selection_posts s ON s.feed_item_id = sp.feed_item_id
            JOIN properties p ON p.id = sp.property_id
            JOIN feed_items f ON f.id = s.feed_item_id
            LEFT JOIN feed_item_content c ON c.feed_item_id = f.id
            WHERE s.selection_type = 'single'
              AND ST_X(p.location::geometry) BETWEEN $1 AND $2
              AND ST_Y(p.location::geometry) BETWEEN $3 AND $4
            ORDER BY f.id, sp.position
        """, min_lon, max_lon, min_lat, max_lat)


