from asyncpg import Connection
from typing import Optional, Dict

class BaseRepository:
    _conn: Connection

    def __init__(self, conn: Connection):
        self._conn = conn

    async def execute(self, query: str, *args):
        return await self._conn.execute(query, *args)

    async def fetchrow(self, query: str, *args) -> Optional[Dict]:
        row = await self._conn.fetchrow(query, *args)
        return dict(row) if row else None

    async def fetch(self, query: str, *args) -> list[Dict]:
        rows = await self._conn.fetch(query, *args)
        return [dict(r) for r in rows]

    async def fetchval(self, query: str, *args):
        return await self._conn.fetchval(query, *args)

