from app.database.pool import db_pool

from app.database.repositories import (
    UserRepository,
    SelectionRepository,
    EventRepository,
    LinkRepository,
    EducationRepository,

    FeedRepository,
    UserFavouritesRepository
)


from asyncpg import Connection

class UnitOfWork:
    def __init__(self):
        self._conn: Connection | None = None
        self._tx = None

        self.users: UserRepository | None = None
        self.selections: SelectionRepository | None = None
        
        self.events: EventRepository | None = None
        self.links: LinkRepository | None = None
        self.education: EducationRepository | None = None

        self.feed: FeedRepository | None = None
        self.user_favourites: UserFavouritesRepository | None = None
        

    async def __aenter__(self):
        self._conn = await db_pool.pool.acquire()
        self._tx = self._conn.transaction()
        await self._tx.start()

        self.users = UserRepository(self._conn)
        self.selections = SelectionRepository(self._conn)
        self.events = EventRepository(self._conn)
        self.links = LinkRepository(self._conn)
        self.education = EducationRepository(self._conn)
        self.feed = FeedRepository(self._conn)
        self.user_favourites = UserFavouritesRepository(self._conn)

        return self

    async def __aexit__(self, exc_type, exc, tb):
        try:
            if exc_type:
                await self._tx.rollback()
            else:
                await self._tx.commit()
        finally:
            await db_pool.pool.release(self._conn)
