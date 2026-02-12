from typing import Optional, List
from datetime import datetime

from app.database.base import BaseRepository
from app.models.event import EventSummary, EventDetail


class EventRepository(BaseRepository):
    async def get_by_id(self, event_id: int) -> Optional[EventDetail]:
        row = await self.fetchrow(
            """
            SELECT
                id,
                name,
                speaker,
                address,
                description,
                signup_link,
                event_at,
                created_at,
                ST_Y(location::geometry) AS latitude,
                ST_X(location::geometry) AS longitude
            FROM events
            WHERE id = $1
            """,
            event_id,
        )

        if not row:
            return None

        return EventDetail(**row)

    async def get_list(
        self,
        limit: int = 20,
        cursor_event_at: Optional[datetime] = None,
        cursor_id: Optional[int] = None,
    ) -> List[EventSummary]:
        if cursor_event_at and cursor_id:
            rows = await self.fetch(
                """
                SELECT
                    id,
                    name,
                    speaker,
                    address,
                    description,
                    signup_link,
                    event_at,
                    ST_Y(location::geometry) AS latitude,
                    ST_X(location::geometry) AS longitude
                FROM events
                WHERE event_at > now()
                AND (event_at, id) > ($1, $2)
                ORDER BY event_at ASC, id ASC
                LIMIT $3
                """,
                cursor_event_at,
                cursor_id,
                limit,
            )
        else:
            rows = await self.fetch(
                """
                SELECT
                    id,
                    name,
                    speaker,
                    address,
                    description,
                    signup_link,
                    event_at,
                    ST_Y(location::geometry) AS latitude,
                    ST_X(location::geometry) AS longitude
                FROM events
                WHERE event_at > now()
                ORDER BY event_at ASC, id ASC
                LIMIT $1
                """,
                limit,
            )

        return [EventSummary(**row) for row in rows]


    async def search(
        self,
        *,
        q: str,
        limit: int = 20,
        cursor_event_at: Optional[datetime] = None,
        cursor_id: Optional[int] = None,
    ) -> List[EventSummary]:
        pattern = f"{q}%"

        if cursor_event_at and cursor_id:
            rows = await self.fetch(
                """
                SELECT
                    id,
                    name,
                    speaker,
                    address,
                    description,
                    signup_link,
                    event_at,
                    ST_Y(location::geometry) AS latitude,
                    ST_X(location::geometry) AS longitude
                FROM events
                WHERE event_at > now()
                AND (name ILIKE $1 OR speaker ILIKE $1 OR address ILIKE $1 OR description ILIKE $1)
                AND (event_at, id) > ($2, $3)
                ORDER BY event_at ASC, id ASC
                LIMIT $4
                """,
                pattern,
                cursor_event_at,
                cursor_id,
                limit,
            )
        else:
            rows = await self.fetch(
                """
                SELECT
                    id,
                    name,
                    speaker,
                    address,
                    description,
                    signup_link,
                    event_at,
                    ST_Y(location::geometry) AS latitude,
                    ST_X(location::geometry) AS longitude
                FROM events
                WHERE event_at > now()
                AND (name ILIKE $1 OR speaker ILIKE $1 OR address ILIKE $1 OR description ILIKE $1)
                ORDER BY event_at ASC, id ASC
                LIMIT $2
                """,
                pattern,
                limit,
            )

        return [EventSummary(**row) for row in rows]
