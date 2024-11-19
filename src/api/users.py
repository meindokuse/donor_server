from fastapi import APIRouter, HTTPException

from src.api.dependencies import UOWDep
from src.config import ROOT_DIR
from src.schemas.auth import UserCreate
from src.services.user_service import UserService

from fastapi.responses import FileResponse
import pandas as pd
import asyncpg
import tempfile
import os

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


# @router.post("/register_request")
# async def add_register_request(
#         register_request: RegRequestCreate,
#         uow: UOWDep,
# ):
#     try:
#         hashed_password = hash_password(register_request.password)
#
#         new_request = RegRequestCreate(
#             telegram_id=register_request.telegram_id,
#             name=register_request.name,
#             email=register_request.email,
#             password=hashed_password,
#         )
#
#         reg_id = await RegRequestService().add_request(uow, new_request)
#         return {
#             "status": "success",
#             "id": reg_id
#         }
#     except Exception as e:
#         return {"status": "error", "msg": str(e)}
#
#
# @router.get("/get_requests")
# async def get_register_requests(
#         uow: UOWDep,
#         page: int,
#         limit: int,
# ):
#     try:
#         requests = await RegRequestService().get_requests(uow, page, limit)
#
#         response = [
#             RegRequestRead(
#                 id=r.id,
#                 telegram_id=r.telegram_id,
#                 name=r.name,
#                 email=r.email,
#             )
#             for r in requests
#         ]
#
#         return {"status": "success", "requests": response}
#     except Exception as e:
#         return {"status": "error", "msg": str(e)}


@router.post("/register")
async def register(user_create: UserCreate, uow: UOWDep):
    try:
        user_id = await UserService().add_user(uow, user_create)

        return {"status": "success", "user": {"id": user_id, "name": user_create.name}}

    except Exception as e:
        raise {
            'status': str(e),
        }


@router.get("/login")
async def login(telegram_id: str, uow: UOWDep):
    try:
        user = await UserService().get_user(uow, telegram_id)

        return {"status": "success", "user": user}

    except Exception as e:
        raise {
            "status": "fail",
        }


@router.get("/check_exist")
async def check_exist(name: str, uow: UOWDep):
    try:
        user = await UserService().get_user_by_name(uow, name)
        if user is None:
            return {"status": "success", "is_exist": False}
        else:
            return {"status": "success", "is_exist": True}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.get("/get_table")
async def get_table(uow: UOWDep):
    try:
        donations = await UserService().get_table_users(uow)

        # Преобразуем данные в DataFrame
        df = pd.DataFrame([dict(row) for row in donations])

        # Путь до временной директории
        temp_dir = os.path.join(ROOT_DIR, 'temp')

        # Создаем папку, если ее нет
        os.makedirs(temp_dir, exist_ok=True)

        # Указываем полный путь для файла
        filename = os.path.join(temp_dir, "donations.xlsx")

        # Сохраняем DataFrame в Excel файл
        df.to_excel(filename, index=False)

        # Отправляем файл пользователю
        response = FileResponse(filename,
                                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                filename="donations.xlsx")

        return response
    except Exception as e:
        raise {
            'status': 'error',
            'message': 'qweqw'
        }
