from typing import Optional
from database.base import BaseRepository


class UserProfileRepository(BaseRepository):

    async def upsert(
        self,
        *,
        user_id: int,
        name: Optional[str] = None,
        phone_number: Optional[str] = None,
        city: Optional[str] = None,
        email: Optional[str] = None,
        telegram_photo_id: Optional[str] = None,
    ) -> dict:
        query = """
        INSERT INTO user_profiles (
            user_id,
            name,
            phone_number,
            city,
            email,
            telegram_photo_id
        )
        VALUES ($1, $2, $3, $4, $5, $6)
        ON CONFLICT (user_id) DO UPDATE SET
            name = EXCLUDED.name,
            phone_number = EXCLUDED.phone_number,
            city = EXCLUDED.city,
            email = EXCLUDED.email,
            telegram_photo_id = EXCLUDED.telegram_photo_id
        RETURNING *
        """
        row = await self._conn.fetchrow(
            query,
            user_id,
            name,
            phone_number,
            city,
            email,
            telegram_photo_id,
        )
        return dict(row)

    async def get(self, user_id: int) -> Optional[dict]:
        query = """
        SELECT *
        FROM user_profiles
        WHERE user_id = $1
        """
        return await self.fetchrow(query, user_id)

    async def delete(self, user_id: int) -> None:
        query = """
        DELETE FROM user_profiles
        WHERE user_id = $1
        """
        await self.execute(query, user_id)
