from fastapi import APIRouter, HTTPException

from app.utils.telegram import verify_init_data
from app.services.auth import create_jwt

router = APIRouter(prefix="/auth", tags=['auth'])

@router.get("/")
async def get_jwt(
        initData: str
    ):
    # data = verify_init_data(initData)
    
    # if not data:
    #     raise HTTPException(
    #         status_code=403,
    #         detail={"error_code": "INVALID_INIT_DATA"},
    #     )

    # telegram_id = int(data["user.id"])

    # TODO: upsert пользователя в БД
    user_id = 1
    subscription_active = False

    token = create_jwt(
        user_id=user_id,
        subscription_active=subscription_active,
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }
