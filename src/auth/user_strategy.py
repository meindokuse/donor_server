from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.auth import UserRead
from src.auth.utils import get_user_by_telegram_id


__all__ = ['get_user']


class _UserStrategy(ABC):
    @abstractmethod
    async def get_current_user(self, telegram_id: Optional[str], session:AsyncSession) -> UserRead:
        pass


class _TelegramUserStrategy(_UserStrategy):
    async def get_current_user(self, telegram_id: Optional[str],session: AsyncSession):
        if telegram_id:
            user = await get_user_by_telegram_id(telegram_id,session)
            return user
        raise ValueError("Invalid or missing telegram_user_id")


# class _SiteUserStrategy(_UserStrategy):
#     async def get_current_user(self, request: Request, user=Depends(current_user)):
#         return user


class _UserContext:
    def __init__(self, strategy: _UserStrategy):
        self.strategy = strategy

    async def get_current_user(self, telegram_id: Optional[str],session: AsyncSession):
        return await self.strategy.get_current_user(telegram_id,session)


async def _select_user_strategy(telegram_id: Optional[str]):
    # if "telegram_user_id" in request.query_params:
    #     return _TelegramUserStrategy()
    # else:
    #     return _SiteUserStrategy()
    return _TelegramUserStrategy()


async def get_user(telegram_id: Optional[str],session:AsyncSession):
    strategy = await _select_user_strategy(telegram_id)
    context = _UserContext(strategy)
    current_user = await context.get_current_user(telegram_id,session)
    return current_user
