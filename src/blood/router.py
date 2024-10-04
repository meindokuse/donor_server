from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.auth.user_strategy import get_user
from src.blood.models import Donation
from src.blood.shemas import DonationCreate, DonationGet

router = APIRouter(
    prefix="/router",
    tags=["router"],
)


@router.post("/add_donation")
async def add_donation(donation: DonationCreate, session: AsyncSession = Depends(get_async_session)):
    session.add(donation)
    await session.commit()
    await session.refresh(donation)

    return {"status": "success"}


@router.get("/get_donations")
async def get_donations_for_user(request: Request, session: AsyncSession = Depends(get_async_session)):
    try:
        user = await get_user(request)
        stmt = select(Donation).where(Donation.user_id == user.id)
        result = await session.execute(stmt)
        data = result.fetchall()

        donations = [
            DonationGet(
                owner=donation.owner,
                group=donation.group,
                rezus=donation.tromb,
                plazma=donation.group,
                date=donation.date,
                org=donation.org,
                tromb=donation.tromb,
            )
            for donation in data
        ]

        return {"status": "success", "donations": donations}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
