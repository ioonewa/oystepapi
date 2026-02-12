from pydantic import BaseModel
from app.models.feed import FeedItemCardDTO

class SelectionMapItem(BaseModel):
    location: dict  # GeoJSON
    item: FeedItemCardDTO
