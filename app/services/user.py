from app.core.config import settings
from app.database.unit_of_work import UnitOfWork

from app.models.user import UserDTO

class UserService:
    uow: UnitOfWork

    def __init__(self, uow: UnitOfWork):
        self.uow=uow

    async def get_refferal_link(self, user_id: int) -> str:
        user_dto = await self.uow.users.get_by_id(user_id)
        user = UserDTO(**user_dto)

        return f"https://t.me/oystep_bot?start=ref_{user.telegram_id}"

    def get_2gis_token(self):
        return settings.map_service_token