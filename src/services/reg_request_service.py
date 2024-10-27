from fastapi import HTTPException

from sqlalchemy import Exists

from src.schemas.auth import RegRequestCreate
from src.utils.unitofwork import IUnitOfWork


class RegRequestService:

    async def add_request(self, uow: IUnitOfWork, reg_request: RegRequestCreate):
        reg_request_dict = reg_request.model_dump()

        async with uow:
            exist_user = await uow.users.find_one(telegram_id=reg_request.telegram_id)
            if exist_user:
                raise HTTPException(status_code=401, detail="Пользователь с таким telegram id уже существует")

            exist_user = await uow.users.find_one(email=reg_request.email)
            if exist_user:
                raise HTTPException(status_code=401, detail="Пользователь с таким email уже существует")

            exist_request = await uow.reg_request.find_one(telegram_id=reg_request.telegram_id)
            if exist_request:
                raise HTTPException(status_code=401, detail="Заявка уже подана")

            exist_request = await uow.reg_request.find_one(email=reg_request.email)
            if exist_request:
                raise HTTPException(status_code=401, detail="Заявка уже подана, такой email, уже есть в нашей базе)")

            reg_request = await uow.reg_request.add_one(reg_request_dict)
            await uow.commit()
            return reg_request

    async def get_requests(self, uow: IUnitOfWork, page, limit):
        async with uow:
            user = await uow.reg_request.find_all(page, limit)
            return user

    async def delete_request(self, uow: IUnitOfWork, telegram_id: str):
        async with uow:
            await uow.reg_request.delete_request(telegram_id)
            await uow.commit()
