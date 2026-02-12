from fastapi import APIRouter, HTTPException
from typing import List
from app.database.unit_of_work import UnitOfWork
from app.services.education import EducationService
from app.models.education import CourseSummary, CourseDetail, LessonDetail

router = APIRouter(prefix="/education", tags=["education"])

@router.get(
    "/courses",
    response_model=List[CourseSummary],
    summary="Список всех курсов",
    description="Возвращает список всех курсов с авторами и количеством уроков"
)
async def get_all_courses():
    async with UnitOfWork() as uow:
        service = EducationService(uow)
        return await service.list_courses()

@router.get(
    "/courses/{course_id}",
    response_model=CourseDetail,
    summary="Детали курса",
    description="Возвращает полную информацию о курсе, включая уроки, авторов и общую длительность"
)
async def get_course_details(course_id: int):
    async with UnitOfWork() as uow:
        service = EducationService(uow)
        course = await service.get_course_detail(course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        return course
    
@router.get(
    "/courses/{course_id}/lessons/{lesson_id}",
    response_model=LessonDetail,
    summary="Детали урока",
    description="Возвращает информацию об уроке, включая ссылки на видео, предыдущий и следующий урок"
)
async def get_lesson_details(course_id: int, lesson_id: int):
    async with UnitOfWork() as uow:
        service = EducationService(uow)
        lesson = await service.get_lesson_detail(course_id, lesson_id)
        if not lesson:
            raise HTTPException(status_code=404, detail="Lesson not found")
        return lesson
    
@router.get(
    "/courses/{course_id}/lessons/{lesson_id}",
    response_model=LessonDetail,
    summary="Детали урока",
    description="Возвращает информацию об уроке, включая ссылки на видео, предыдущий и следующий урок"
)
async def get_lesson_details(feed_item_id: int, lesson_id: int):
    async with UnitOfWork() as uow:
        service = EducationService(uow)
        lesson = await service.get_lesson_detail(course_id, lesson_id)
        if not lesson:
            raise HTTPException(status_code=404, detail="Lesson not found")
        return lesson

