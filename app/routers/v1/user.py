from fastapi import APIRouter, Depends
from app.services.user import UserService
from app.dependencies.auth import get_current_user
from app.database.unit_of_work import UnitOfWork

from app.core.config import settings

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/refferal_link")
async def get_refferal_link(
    current_user=Depends(get_current_user),
):
    async with UnitOfWork() as uow:
        service = UserService(uow)
        referral_link = await service.get_refferal_link(current_user.id)
        
        return {"refferal_link": 'Не доступно'} # Починить авторизацию


@router.get("/map_token")
async def get_map_token():
    async with UnitOfWork() as uow:
        service = UserService(uow)
        map_token = service.get_2gis_token()
        return {"map_token": map_token}
