import jwt

from app.core import settings
from datetime import datetime, timedelta, timezone
from typing import Optional


def create_jwt(*, user_id: int, subscription_active: bool) -> str:
    payload = {
        "user_id": str(user_id),
        "subscription_active": subscription_active,
        "iat": datetime.now(tz=timezone.utc),
        "exp": datetime.now(tz=timezone.utc)
        + timedelta(seconds=settings.jwt_ttl_seconds),
    }

    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_jwt(token: str) -> Optional[dict]:
    try:
        return jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )
    except Exception:
        return None
