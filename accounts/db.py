import datetime
from uuid import UUID

from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    if email is None:
        return
    res = await session.execute(select(User).where(User.email == email))
    return res.scalar()


async def get_user_by_uuid(session: AsyncSession, uuid: UUID) -> User | None:
    res = await session.execute(select(User).where(User.uuid == uuid))
    return res.scalar()


async def create_user(session: AsyncSession, full_name: str, email: str, password_hash: str) -> UUID:
    statement = insert(User) \
        .values({'full_name': full_name, 'email': email, 'password_hash': password_hash}) \
        .returning(User.uuid)
    res = await session.execute(statement)
    await session.commit()
    return res.scalar()


async def update_user_email(session: AsyncSession, uuid: UUID, email: str) -> None:
    await session.execute(update(User).where(User.uuid == uuid).values({'email': email}))
    await session.commit()


async def update_user_last_login(session: AsyncSession, uuid: UUID) -> None:
    await session.execute(
        update(User).where(User.uuid == uuid).values({'last_login': datetime.datetime.now()})
    )
    await session.commit()
