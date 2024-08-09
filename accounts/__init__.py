import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from accounts.db import get_user_by_uuid
from accounts.utils import authenticate, encode_jwt, decode_jwt
from db.dependencies import get_async_session
from db.models import User

router = APIRouter(prefix='/accounts')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/accounts/login')


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        db_session: Annotated[AsyncSession, Depends(get_async_session)]
) -> User | None:
    payload = decode_jwt(token, required_keys=['uuid'])
    if payload is None:
        return
    uuid = UUID(payload['uuid'])
    return await get_user_by_uuid(db_session, uuid)


async def get_current_user_or_401(current_user: Annotated[User | None, Depends(get_current_user)]):
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Unauthorized'
        )
    return current_user


@router.post('/login')
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db_session: Annotated[AsyncSession, Depends(get_async_session)]
):
    user = await authenticate(db_session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='login or password incorrect'
        )
    token = encode_jwt({'uuid': user.uuid.hex}, expires=datetime.timedelta(weeks=52))
    return {'token_type': 'bearer', 'access_token': token}
