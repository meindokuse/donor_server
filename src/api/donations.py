from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from src.api.dependencies import UOWDep
from src.schemas.donations import DonationCreate
from src.services.donation_service import DonationService
from src.services.user_service import UserService

router = APIRouter(
    prefix="/donation",
    tags=["donation"],
)


# ЭНДПОИНТЫ ДЛЯ ОБЫЧНЫХ ПОЛЬЗОВАТЕЛЕЙ
@router.get("/get_donation_info")
async def get_donations_info_from_user(
        uow: UOWDep,
        telegram_id: Optional[str] = Query(None),
):
    try:
        donation_info = await DonationService().get_donations_info_from_user(uow, telegram_id)
        user = await UserService().get_user(uow, telegram_id)

        return {
            "status": "success",
            "user": user,
            "donation_info": donation_info
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
                "message": "Донаций не найдено"
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


@router.get("/admin/get_all_donations")
async def get_all_donations(
        uow: UOWDep,
        page: int,
        limit: int,
        start_date: str,
        end_date: str,
        type_donation: Optional[str] = Query(None),

):
    try:
        donations_info = await DonationService().get_all_donations(uow, start_date, end_date, page, limit,
                                                                   type_donation)

        return {
            "status": "success",
            "data": donations_info,
        }

    except Exception as e:
        raise {
            "status": "error",
            "message": str(e)
        }


@router.get("/admin/get_donations_info_from_user")
async def get_donations_info_from_user(
        uow: UOWDep,
        name: str,
):
    try:
        donation_info = await DonationService().get_donations_info_from_user(uow, name=name)
        user = await UserService().get_user_by_name(uow, name)

        return {
            "status": "success",
            "user": user,
            "donation_info": donation_info
        }

    except Exception as e:
        return {
            'status': 'error',
            'details': e
        }
