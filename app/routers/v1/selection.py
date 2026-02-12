from fastapi import APIRouter, Query
from typing import List
from app.database.unit_of_work import UnitOfWork
from app.services.selection import SelectionService
from app.models.selection import SelectionMapItem

router = APIRouter(prefix="/selections", tags=["Selections"])

@router.get("/map", response_model=List[SelectionMapItem])
async def get_selections_map(
    min_lon: float = Query(...),
    min_lat: float = Query(...),
    max_lon: float = Query(...),
    max_lat: float = Query(...),
):
    async with UnitOfWork() as uow:
        service = SelectionService(uow)
        return await service.get_map_items(min_lon, min_lat, max_lon, max_lat)