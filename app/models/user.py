from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserDTO(BaseModel):
    id: int
    telegram_id: int
    username: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[datetime]= None