from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.auth import Users
from src.schemas.auth import UserRead

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password):
    return pwd_context.hash(password)


async def get_user_by_telegram_id(telegram_id: str, session: AsyncSession):
    if not telegram_id:
        raise HTTPException(status_code=400, detail="telegram_id must be provided")

    try:
        stmt = select(Users).where(Users.telegram_id == telegram_id)
        result = await session.execute(stmt)
        user = result.scalars().first()


        return user

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: " + str(e))


async def get_user_by_name(name: str, session: AsyncSession):
    stmt = select(Users).where(Users.name == name)
    data = await session.execute(stmt)
    user = data.scalars().first()
    if user is None:
        return None
    user_read = UserRead(
        name=user.name,
        telegram_id=user.telegram_id,
        email=user.email,
        role_id=user.role_id,
        registered_on=user.registered_at,
    )
    return user_read
