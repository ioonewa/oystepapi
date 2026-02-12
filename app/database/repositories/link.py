from typing import Optional, List

from app.database.base import BaseRepository
from app.models.link import Link


class LinkRepository(BaseRepository):
    async def get_by_id(self, id: int) -> Optional[Link]:
        row = await self.fetchrow(
            """
            SELECT
                id,
                name,
                telegram_username,
                link,
                type,
                tag,
                preview,
                main_color,
                border_color,
                created_at
            FROM links
            WHERE id = $1
            """,
            id,
        )

        if not row:
            return None

        return Link(**row)

    async def get_list(self) -> List[Link]:
        rows = await self.fetch(
            """
            SELECT
                id,
                name,
                telegram_username,
                link,
                type,
                tag,
                preview,
                main_color,
                border_color,
                created_at
            FROM links
            ORDER BY position 
            LIMIT 100
            """
        )

        return [Link(**row) for row in rows]
