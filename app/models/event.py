from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class EventBase(BaseModel):
    name: str = Field(
        ...,
        description="Название мероприятия"
    )
    speaker: Optional[str] = Field(
        None,
        description="Имя спикера или ведущего мероприятия"
    )
    address: Optional[str] = Field(
        None,
        description="Физический адрес проведения мероприятия"
    )
    description: Optional[str] = Field(
        None,
        description="Описание мероприятия"
    )
    signup_link: Optional[str] = Field(
        None,
        description="Ссылка на регистрацию или покупку билета"
    )
    event_at: datetime = Field(
        ...,
        description="Дата и время проведения мероприятия"
    )
    latitude: Optional[float] = Field(
        None,
        description="Широта места проведения (для отображения на карте)",
        ge=-90,
        le=90
    )
    longitude: Optional[float] = Field(
        None,
        description="Долгота места проведения (для отображения на карте)",
        ge=-180,
        le=180
    )


class EventSummary(EventBase):
    id: int = Field(
        ...,
        description="Уникальный идентификатор мероприятия"
    )


class EventDetail(EventBase):
    id: int = Field(
        ...,
        description="Уникальный идентификатор мероприятия"
    )
    created_at: datetime = Field(
        ...,
        description="Дата и время создания мероприятия"
    )
