from src.models.auth import Users
from src.data.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = Users

