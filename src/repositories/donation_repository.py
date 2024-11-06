from sqlalchemy import select

from src.models.donations import Donation
from src.data.repository import SQLAlchemyRepository


class DonationRepository(SQLAlchemyRepository):
    model = Donation

    async def get_donations_by_date(self, start_date, end_date, page, limit):
        if limit == 0:
            query = (
                select(self.model)
                .where(Donation.date >= start_date, Donation.date <= end_date)
            )
            result = await self.session.execute(query)

            return result.all()

        offset = (page - 1) * limit

        query = (
            select(self.model)
            .where(Donation.date >= start_date, Donation.date <= end_date)
            .order_by(Donation.date.asc())
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)

        res = [row[0].to_read_model() for row in result.all()]

        return res
