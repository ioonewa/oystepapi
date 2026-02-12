import asyncpg
from app.core import settings

class DatabasePool:
    def __init__(self):
        self._pool: asyncpg.Pool | None = None

    async def connect(self):
        self._pool = await asyncpg.create_pool(
            host=settings.db_host,
            port=settings.db_port,
            user=settings.db_user,
            password=settings.db_password,
            database=settings.db_name,
        )


    async def disconnect(self):
        if self._pool:
            await self._pool.close()

    @property
    def pool(self) -> asyncpg.Pool:
        if not self._pool:
            raise RuntimeError("Database pool is not initialized")
        return self._pool


db_pool = DatabasePool()
