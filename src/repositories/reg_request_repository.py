from sqlalchemy import delete

from src.models.auth import RegRequest
from src.data.repository import SQLAlchemyRepository


class RegRequestRepository(SQLAlchemyRepository):
    model = RegRequest

    async def delete_request(self, request_id: str):
        stmt = delete(self.model).where(self.model.telegram_id == request_id)
        await self.session.execute(stmt)
