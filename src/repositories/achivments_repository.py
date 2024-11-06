from src.data.repository import SQLAlchemyRepository
from src.models.auth import Achievement


class AchievementRepository(SQLAlchemyRepository):
    model = Achievement
