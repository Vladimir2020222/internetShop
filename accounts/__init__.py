import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Form, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from accounts.db import get_user_by_uuid, create_user, update_user_email, update_user_last_login
from accounts.hashers import hash_password
from accounts.utils import authenticate, encode_jwt, decode_jwt
from db.dependencies import get_async_session
from db.models import User
from mail import send_email

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
    await update_user_last_login(db_session, user.uuid)
    return {'token_type': 'bearer', 'access_token': token}


@router.post('/signup')
async def sign_up(
        full_name: Annotated[str, Form()],
        email: Annotated[str, Form()],
        password: Annotated[str, Form()],
        confirm_email_url_template: str,
        db_session: Annotated[AsyncSession, Depends(get_async_session)]
):
    password_hash = await hash_password(password)
    uuid = await create_user(db_session, full_name, email, password_hash)
    payload = {
        'uuid': uuid,
        'email': email
    }
    token = encode_jwt(payload, datetime.timedelta(minutes=30))
    url = confirm_email_url_template.replace("$TOKEN$", token)
    await send_email(email, f'to confirm email follow this link: {url}')


@router.post('/confirm_email')
async def confirm_email(
        token: Annotated[str, Body()],
        db_session: Annotated[AsyncSession, Depends(get_async_session)]
):
    payload = decode_jwt(token, ['uuid', 'email'])
    if payload is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='invalid token')
    uuid = payload['uuid']
    email = payload['email']
    await update_user_email(db_session, uuid, email)
