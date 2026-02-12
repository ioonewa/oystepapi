import hmac
import hashlib
from urllib.parse import parse_qsl

from app.core.config import settings

def verify_init_data(init_data: str) -> dict | None:
    try:
        data = dict(parse_qsl(init_data, strict_parsing=True))
    except Exception as ex:
        return None
    
    received_hash = data.pop("hash", None)

    if not received_hash:
        return None

    check_string = "\n".join(f"{k}={v}" for k, v in sorted(data.items()))
    secret_key = hashlib.sha256(settings.bot_token.encode()).digest()

    calculated_hash = hmac.new(
        secret_key,
        check_string.encode(),
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(calculated_hash, received_hash):
        return None

    return data