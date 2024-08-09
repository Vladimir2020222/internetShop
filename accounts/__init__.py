from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix='/accounts')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/accounts/login')
