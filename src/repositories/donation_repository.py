from src.models.donations import Donation
from src.utils.repository import SQLAlchemyRepository


class DonationRepository(SQLAlchemyRepository):
    model = Donation




