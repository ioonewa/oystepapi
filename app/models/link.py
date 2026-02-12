from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class ChatTag(str, Enum):
    project = "project"
    partner = "partner"


class ChatType(str, Enum):
    group = "group"
    channel = "channel"
    bot = "bot"


class Link(BaseModel):
    id: int = Field(
        ...,
        description="Уникальный идентификатор ссылки"
    )

    name: str = Field(
        ...,
        description="Отображаемое название блока или чата"
    )
    telegram_username: Optional[str] = Field(
        None,
        description="Telegram username (без @), если есть"
    )
    link: str = Field(
        ...,
        description="Полная ссылка на Telegram-чат, канал или бота"
    )
    type: ChatType = Field(
        ...,
        description="Тип Telegram-сущности: группа, канал или бот"
    )
    tag: ChatTag = Field(
        ...,
        description="Категория ссылки"
    )

    preview: Optional[str] = Field(
        None,
        description="URL изображения-превью для блока"
    )
    main_color: Optional[str] = Field(
        None,
        description="Основной цвет блока HEX"
    )
    border_color: Optional[str] = Field(
        None,
        description="Цвет рамки блока HEX"
    )

    created_at: datetime = Field(
        ...,
        description="Дата и время создания ссылки"
    )
