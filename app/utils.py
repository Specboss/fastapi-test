import hashlib

from app.core.config import settings


def make_signature(payload: dict) -> str:
    s = f"{payload['account_id']}{payload['amount']}{payload['transaction_id']}{payload['user_id']}{settings.SECRET_KEY}"
    return hashlib.sha256(s.encode()).hexdigest()
