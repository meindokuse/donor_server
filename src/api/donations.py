from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dependencies import UOWDep
from src.auth.utils import get_user_by_name
from src.db.database import get_async_session
from src.auth.user_strategy import get_user
from src.models.donations import Donation
from src.schemas.donations import DonationCreate, DonationRead
from src.services.donation_service import DonationService
from src.services.user_service import UserService

router = APIRouter(
    prefix="/router",
    tags=["router"],
)


# ЭНДПОИНТЫ ДЛЯ ОБЫЧНЫХ ПОЛЬЗОВАТЕЛЕЙ
@router.get("/get_donations_info_from_user")
async def get_donations_info_from_user(
        telegram_id: Optional[str],
        uow: UOWDep
):
    try:

        donation_info = await DonationService().get_donations_info_from_user(uow, telegram_id)

        return donation_info

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/get_user_donations")
async def get_user_donations(
        uow: UOWDep,
        page: int,
        limit: int,
        telegram_id: Optional[str] = Query(None),
):
    try:

        user = await UserService().get_user(uow, telegram_id)
        if user:
            data = await DonationService().get_user_donations(uow, user.telegram_id, page, limit)

            return {
                "status": "success",
                "data": data,
            }
        else:
            return {
                "status": "error",
                "message": "Информации не найдено, возможно вы ввели неверные данные"
            }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ЭНДПОИНТЫ ДЛЯ АДМИНОВ

@router.post("/admin/add_donation")
async def add_donation(
        donation_data: DonationCreate,
        uow: UOWDep
):
    try:
        donation_id = await DonationService().add_donation(uow, donation_data)

        return {
            "status": "success",
            "id": donation_id
        }


    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.get("/admin/get_info_donations_all")
async def get_info_donations_all(
        start_date: str,
        end_date: str,
        uow: UOWDep
):
    try:
        info = await DonationService().get_info_donations_period(uow, start_date, end_date)

        return info

    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.get("/admin/get_all_donations")
async def get_all_donations(
        page: int,
        limit: int,
        start_date: str,
        end_date: str,
        uow: UOWDep
):
    try:
        donations = await DonationService().get_all_donations(uow, start_date, end_date, page, limit)
        return {
            "status": "success",
            "data": donations,
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
