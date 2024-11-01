from datetime import datetime, date

from fastapi import HTTPException

from src.models.auth import Users
from src.schemas.auth import UserCreate, UserRead
from src.data.unitofwork import IUnitOfWork


class UserService:

    async def add_user(self, uow: IUnitOfWork, user: UserCreate):
        user_dict = user.model_dump()
        async with uow:
            is_exist = await uow.users.find_one(name = user_dict['name'])
            if is_exist:
                raise HTTPException(status_code=400, detail='Пользователь с таким именем уже есть')
            user_id = await uow.users.add_one(user_dict)
            request_id = user.telegram_id
            await uow.reg_request.delete_request(request_id=request_id)
            await uow.commit()
            return user_id

    async def get_user(self, uow: IUnitOfWork, tg_id: str):
        async with uow:
            user = await uow.users.find_one(telegram_id=tg_id)
            return user
