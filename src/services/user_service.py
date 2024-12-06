from fastapi import HTTPException

from src.schemas.auth import UserCreate, UserRead
from src.data.unitofwork import IUnitOfWork


class UserService:

    async def add_user(self, uow: IUnitOfWork, user: UserCreate):
        user_dict = user.model_dump()
        async with uow:
            is_exist = await uow.users.find_one(name=user_dict['name'])
            if is_exist:
                raise HTTPException(status_code=400, detail='Пользователь с таким именем уже есть')
            user_id = await uow.users.add_one(user_dict)
            await uow.commit()
            return user_id

    async def get_user(self, uow: IUnitOfWork, tg_id: str):
        async with uow:
            user = await uow.users.find_one(telegram_id=tg_id)
            return user

    async def get_user_by_name(self, uow: IUnitOfWork, name: str):
        async with uow:
            user = await uow.users.find_one(name=name)
            return user

    async def get_table_users(self, uow: IUnitOfWork):
        async with uow:
            return await uow.users.get_table()

    async def edit_status(self, uow: IUnitOfWork, name: str, points: float):
        async with uow:
            user: UserRead = await uow.users.find_one(name=name)
            status_points = user.status
            status_points += points
            id = user.id

            await uow.users.edit_one(id=id, data={'status': status_points})
            await uow.commit()
