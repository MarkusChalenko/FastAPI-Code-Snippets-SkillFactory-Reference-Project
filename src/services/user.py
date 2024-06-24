from fastapi import HTTPException
from sqlalchemy import select, update, delete
from starlette import status

from auth.auth import bcrypt_context
from db.db import db_dependency
from models import User
from schemas.user import UserCreate, UserRead, UserUpdate


async def create_new_user(db: db_dependency, user_data: UserCreate) -> UserRead:
    create_user_request: User = User(
        login=user_data.login,
        email=user_data.email,
        hashed_password=bcrypt_context.hash(user_data.password)
    )

    db.add(create_user_request)
    await db.commit()

    created_user_data: UserRead = await get_user_by_login(db, user_data.login)

    return created_user_data


async def get_user_by_id(db: db_dependency, user_id: int) -> UserRead:
    statement = select(User).where(User.id == user_id)
    result = await db.execute(statement)
    user: User = result.scalar()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No user with id:{user_id}")
    return user.to_user_read()


async def update_user(db: db_dependency, user_id: int, update_data: UserUpdate) -> UserRead:
    statement = update(User)\
        .where(User.id == user_id)\
        .values(update_data.dict(exclude_unset=True))
    updated_count = await db.execute(statement)
    rows = updated_count.rowcount()
    if rows == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")

    await db.commit()

    updated_user_data: UserRead = await get_user_by_id(db, user_id)
    return updated_user_data


async def delete_user(db: db_dependency, user_id: int) -> None:
    statement = delete(User).where(User.id == user_id)
    deleted_count = await db.execute(statement)

    if deleted_count.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")

    await db.commit()


async def get_user_by_login(db: db_dependency, login: str) -> UserRead:
    statement = select(User).where(User.login == login)
    result = await db.execute(statement)
    user: User = result.scalar()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No user with login:{login}")
    return user.to_user_read()
