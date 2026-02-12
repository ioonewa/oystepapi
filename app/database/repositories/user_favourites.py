from ..base import BaseRepository

class UserFavouritesRepository(BaseRepository):
    async def add_favourite(self, user_id: int, feed_item_id: int):
        await self.execute("""
        INSERT INTO user_favourites(user_id, feed_item_id)
        VALUES ($1, $2)
        ON CONFLICT DO NOTHING
        """, user_id, feed_item_id)

    async def remove_favourite(self, user_id: int, feed_item_id: int):
        await self.execute("""
        DELETE FROM user_favourites
        WHERE user_id = $1 AND feed_item_id = $2
        """, user_id, feed_item_id)

    async def get_user_favourites(self, user_id: int) -> list[int]:
        rows = await self.fetch("""
        SELECT feed_item_id FROM user_favourites
        WHERE user_id = $1
        """, user_id)
        return [r['feed_item_id'] for r in rows]
