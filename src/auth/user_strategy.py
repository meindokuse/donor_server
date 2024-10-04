from abc import ABC, abstractmethod
from fastapi import Request, Depends
from fastapi_users import FastAPIUsers

from src.auth.schemas import UserRead
from src.auth.utils import get_user_by_telegram_id


__all__ = ['get_user']


class _UserStrategy(ABC):
    @abstractmethod
    async def get_current_user(self, request: Request) -> UserRead:
        pass


class _TelegramUserStrategy(_UserStrategy):
    async def get_current_user(self, request: Request):
        telegram_user_id = request.query_params.get("telegram_user_id")
        if telegram_user_id:
            user = await get_user_by_telegram_id(telegram_user_id)
            return user
        raise ValueError("Invalid or missing telegram_user_id")


class _SiteUserStrategy(_UserStrategy):
    async def get_current_user(self, request: Request, user=Depends(current_user)):
        return user


class _UserContext:
    def __init__(self, strategy: _UserStrategy):
        self.strategy = strategy

    async def get_current_user(self, request: Request):
        return await self.strategy.get_current_user(request)


async def _select_user_strategy(request: Request):
    if "telegram_user_id" in request.query_params:
        return _TelegramUserStrategy()
    else:
        return _SiteUserStrategy()


async def get_user(request: Request):
    strategy = await _select_user_strategy(request)
    context = _UserContext(strategy)
    current_user = await context.get_current_user(request)
    return current_user
