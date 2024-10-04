from fastapi import Depends, HTTPException
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.auth.models import User
from src.auth.schemas import UserRead

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password):
    return pwd_context.hash(password)


async def get_user_by_telegram_id(telegram_id, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await session.execute(stmt)
        user = result.scalars().first()
        user_read = UserRead(
            username=user.name,
            email=user.email,
            role_id=user.role_id,
            register_on=user.registered_at
        )
        return user_read

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
