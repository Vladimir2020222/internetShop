import datetime

import jwt
from sqlalchemy.ext.asyncio import AsyncSession

import config
from accounts.db import get_user_by_email
from db.models import User


async def authenticate(session: AsyncSession, email: str, password: str) -> User | None:
    user = await get_user_by_email(session, email)
    if user and await user.check_password(password):
        return user


def encode_jwt(payload: dict, expires: datetime.timedelta) -> str:
    payload.setdefault('exp', datetime.datetime.now() + expires)
    return jwt.encode(payload, config.SECRET_KEY, config.ENCODE_JWT_ALGORITHM)


def decode_jwt(token: str, required_keys: list[str] = None) -> dict | None:
    required_keys = required_keys or []
    if token is None:
        return
    try:
        payload = jwt.decode(token, config.SECRET_KEY, config.DECODE_JWT_ALGORITHMS)
        for key in required_keys:
            if key not in payload:
                return
        return payload
    except jwt.InvalidTokenError:
        return None
