from typing import Optional
from app.database.unit_of_work import UnitOfWork
from app.models.feed import LessonDetail


class EducationService:

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def get_lesson_detail(
            self,
            feed_item_id: int,
            lesson_id: int
        ) -> Optional[LessonDetail]:
        lessons_db = await self.uow.education.get_lessons(feed_item_id)
        lessons_ordered = sorted(lessons_db, key=lambda x: x.position)

        lesson_map = {l.id: l for l in lessons_ordered}
        lesson = lesson_map.get(lesson_id)
        if not lesson:
            return None

        idx = lessons_ordered.index(lesson)
        prev_id = lessons_ordered[idx - 1].id if idx > 0 else None
        next_id = lessons_ordered[idx + 1].id if idx < len(lessons_ordered) - 1 else None

        return LessonDetail(
            id=lesson.id,
            title=lesson.title,
            description=lesson.description,
            video_url=lesson.video_url,
            duration_seconds=lesson.duration_seconds,
            previous_lesson_id=prev_id,
            next_lesson_id=next_id
        )
