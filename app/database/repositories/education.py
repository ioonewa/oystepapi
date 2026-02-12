from typing import Optional, List

from app.database.base import BaseRepository
from app.models.feed import Author, LessonDTO


class LessonsRepository(BaseRepository):
    # ---------------- LESSONS ----------------
    async def get_lessons(
        self,
        feed_item_id: int
    ) -> List[LessonDTO]:
        query = """
            SELECT 
                id,
                course_feed_item_id,
                title,
                description,
                position,
                created_at,
                updated_at
            FROM lessons
            WHERE course_feed_item_id = $1
            ORDER BY position
        """

        rows = await self._conn.fetch(query, feed_item_id)

        return [
            LessonDTO(
                id=row["id"],
                title=row["title"],
                position=row["position"],
            )
            for row in rows
        ]

    async def get_lesson(
            self,
            lesson_id: int
        ) -> Optional[LessonDTO]:
        GET_LESSON_SQL = """
        ...
        """
        row = await self.fetchrow(GET_LESSON_SQL, lesson_id)
        return LessonDTO(**row) if row else None
    
    # ---------------- AUTHORS ----------------

    async def get_authors_by_course(self, feed_item_id: int) -> List[Author]:
        SQL = """
        SELECT a.id, a.name, a.bio, a.avatar_medi_id, a.created_at
        FROM authors a
        JOIN course_authors ca ON ca.author_id = a.id
        WHERE ca.feed_item_id = $1
        ORDER BY a.name
        """
        rows = await self.fetch(SQL, feed_item_id)
        return [Author(**row) for row in rows]
