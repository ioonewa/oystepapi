from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

# --- Медиа ---
class MediaItemDTO(BaseModel):
    id: int
    type: str
    url: str
    preview_url: Optional[str]
    width: Optional[int]
    height: Optional[int]
    duration_seconds: Optional[int]

# --- Кнопка ---
class ButtonDTO(BaseModel):
    text: str
    link: str

# --- Гео объект для properties ---
class PropertyDTO(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float
    address: Optional[str]
    city: Optional[str]

# --- FeedItem DTO для карточки/ленты ---
class FeedItemCardDTO(BaseModel):
    id: int
    type: str
    published_at: datetime
    title: str
    short_description: Optional[str]
    preview_media_id: int
    media: List[MediaItemDTO]
    is_favourite: bool

class FeedPageDTO(BaseModel):
    items: List[FeedItemCardDTO]
    next_cursor: Optional[str] = None

# --- Контент конкретного типа selection ---
class LessonDTO(BaseModel):
    id: int

    course_feed_item_id: int

    title: int
    description: Optional[str]

    position: int

    created_at: datetime
    updated_at: datetime

class SelectionContentDTO(BaseModel):
    selection_type: str
    properties: Optional[List[PropertyDTO]] = []
    related_selections: Optional[List[FeedItemCardDTO]] = []

class Author(BaseModel):
    id: int
    name: str
    bio: Optional[str]
    avatar_url: Optional[str]
    created_at: datetime

    

class LessonDetail(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор урока")
    title: str = Field(..., description="Название урока")
    description: Optional[str] = Field(None, description="Описание урока")
    video_url: Optional[str] = Field(None, description="Ссылка на видео урока")
    preview_url: Optional[str] = Field(None, description="Ссылка на превью урока")
    duration_seconds: Optional[int] = Field(None, description="Длительность урока в секундах")
    previous_lesson_id: Optional[int] = Field(None, description="ID предыдущего урока в курсе")
    next_lesson_id: Optional[int] = Field(None, description="ID следующего урока в курсе")


class LessonShort(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор урока")
    title: str = Field(..., description="Название урока")
    position: int = Field(..., description="Порядок урока в курсе")

# --- Контент конкретного типа course ---
class CourseContentDTO(BaseModel):
    authors: Optional[List[Author]]
    lessons: Optional[List[LessonShort]]

class FeedItemPageDTO(FeedItemCardDTO):
    body: Optional[str]
    button: Optional[ButtonDTO]
    
    # Тип "Объекты"
    selection: Optional[SelectionContentDTO]

    # Тип "Обучение"
    course: Optional[CourseContentDTO]
    

# --- Категории постов ---
class FeedItemTypeDTO(BaseModel):
    code: str
    title: str
