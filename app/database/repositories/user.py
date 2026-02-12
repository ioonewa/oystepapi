from typing import Optional, List
from database.base import BaseRepository


class UserRepository(BaseRepository):
    async def add(
        self,
        *,
        telegram_id: int,
        username: Optional[str] = None,
        status: Optional[str] = None,
    ) -> dict:
        query = """
        INSERT INTO users (telegram_id, username, status)
        VALUES ($1, $2, $3)
        RETURNING *
        """
        row = await self._conn.fetchrow(
            query,
            telegram_id,
            username,
            status,
        )
        return dict(row)

    async def get_by_id(self, user_id: int) -> Optional[dict]:
        query = """
        SELECT *
        FROM users
        WHERE id = $1
        """
        return await self.fetchrow(query, user_id)

    async def get_by_telegram_id(self, telegram_id: int) -> Optional[dict]:
        query = """
        SELECT *
        FROM users
        WHERE telegram_id = $1
        """
        return await self.fetchrow(query, telegram_id)

    async def update_status(self, user_id: int, status: str) -> Optional[dict]:
        query = """
        UPDATE users
        SET status = $2
        WHERE id = $1
        RETURNING *
        """
        return await self.fetchrow(query, user_id, status)

