from abc import ABC, abstractmethod
from typing import Type

from src.db.database import async_session_maker
from src.repositories.donation_repository import DonationRepository
from src.repositories.reg_request_repository import RegRequestRepository
from src.repositories.user_repository import UserRepository


# https://github1s.com/cosmicpython/code/tree/chapter_06_uow
class IUnitOfWork(ABC):
    users: Type[UserRepository]
    reg_request: Type[RegRequestRepository]
    donations: Type[DonationRepository]

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, *args):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...


class UnitOfWork:
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()

        self.users = UserRepository(self.session)
        self.reg_request = RegRequestRepository(self.session)
        self.donations = DonationRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()