from datetime import timedelta, datetime
from typing import Annotated, Dict
from calendar import timegm

from fastapi import HTTPException, Depends
from sqlalchemy import select

from jose import jwt, JWTError
from starlette import status

from auth.auth import bcrypt_context, oauth2_bearer
from core.config import app_settings
from db.db import db_dependency
from models import User


async def authenticate_user(login: str, password: str, db: db_dependency) -> User | bool:
    statement = select(User).where(User.login == login)
    result = await db.execute(statement)
    user = result.scalars().first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(login: str, user_id: int, expires_delta: timedelta) -> str:
    encode = {'sub': login, 'id': user_id}
    expires = timegm((datetime.utcnow() + expires_delta).utctimetuple())
    encode.update({'exp': expires})
    return jwt.encode(encode, app_settings.jwt_secret, algorithm=app_settings.algorithm)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload: dict = jwt.decode(token, app_settings.jwt_secret,
                                   algorithms=app_settings.algorithm)
        user_name: str = payload.get('sub')
        user_id: int = payload.get('id')
        if user_name is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Could not validate user.")
        return {'username': user_name, 'id': user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate user.")


user_dependency = Annotated[dict, Depends(get_current_user)]
