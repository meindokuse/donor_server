from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.auth.models import User, RegRequest
from src.auth.schemas import UserCreate, RegRequestCreate, RegRequestRead
from src.auth.user_strategy import get_user
from src.auth.utils import hash_password

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.post("/register_request")
async def add_register_request(register_request: RegRequestCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        if register_request.email is not None:
            stmt = select(User).where(User.telegram_id == register_request.telegram_id)
        else:
            stmt = select(User).where(User.email == register_request.email)
        result = await session.execute(stmt)
        existing_user = result.scalar_one_or_none()
        if existing_user:
            raise HTTPException(status_code=400, detail="User with this email already exists")
        hashed_password = hash_password(register_request.password)

        new_request = RegRequest(
            telegram_id=register_request.telegram_id,
            name=register_request.name,
            email=register_request.email,
            password=hashed_password,
        )

        session.add(new_request)
        await session.commit()
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "msg": str(e)}


@router.get("/get_requests")
async def get_register_requests(session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = select(RegRequest)
        result = await session.execute(stmt)
        requests = result.scalars().all()

        response = [
            RegRequestRead(
                telegram_id=r.telegram_id,
                name=r.name,
                email=r.email,
                password=r.password
            )
            for r in requests
        ]

        return {"status": "success", "requests": response}
    except Exception as e:
        return {"status": "error", "msg": str(e)}


@router.post("/register")
async def register(user: UserCreate, session: AsyncSession = Depends(get_async_session)):
    new_user = User(
        telegram_id=user.telegram_id,
        name=user.username,
        email=user.email,
        password=user.password,
        role_id=2,
        registered_at=datetime.utcnow()
    )

    session.add(new_user)
    await session.commit()

    return {"status": "success"}


@router.get("/login")
async def login(request: Request):
    try:
        user_info = await get_user(request)
        return {"status": "success", "user": user_info}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


