from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.services.auth import decode_jwt

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth",
)


class CurrentUser:
    __slots__ = ("id", "subscription_active")

    def __init__(self, *, id: int, subscription_active: bool):
        self.id = id
        self.subscription_active = subscription_active


async def get_current_user(
    token: str = Depends(oauth2_scheme),
) -> CurrentUser:
    payload = decode_jwt(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="INVALID_TOKEN",
        )

    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="INVALID_TOKEN",
        )

    return CurrentUser(
        id=int(user_id),
        subscription_active=payload.get("subscription_active", False),
    )
