from datetime import datetime, timedelta

from sqlalchemy.sql.functions import current_date

from src.schemas.donations import DonationCreate
from src.utils.unitofwork import IUnitOfWork


class DonationService:

    async def get_donations_info_from_user(self, uow: IUnitOfWork, telegram_id: str):

        status:int # проверка для перерыва в донациях в 2 месяца
        today_date = datetime.today().date()
        two_months_ago = today_date - timedelta(days=60)

        async with uow:

            user = await uow.users.find_one(telegram_id=telegram_id)
            name = user.name

            donations = await uow.donations.find_all(page=1, limit=0, owner=name)

            if donations:

                quantity_donation = len(donations)
                last_donation = max(donations, key=lambda donation: donation.id) if donations else None

                last_data = last_donation.date

                status = 1 if last_data <= two_months_ago else 0
            else:
                quantity_donation = 0
                last_donation = "Вы еще не делали донации"
                status = 1

            return {
                "quantity_donation": quantity_donation,
                "last_donation": last_donation,
                "status":status
            }

    async def get_user_donations(
            self,
            uow: IUnitOfWork,
            telegram_id: str,
            page: int,
            limit: int,
    ):
        async with uow:
            user = await uow.users.find_one(telegram_id=telegram_id)
            name = user.name

            donations = await uow.donations.find_all(page=page, limit=limit, owner=name)

            return donations

    async def add_donation(self, uow: IUnitOfWork, donation_data: DonationCreate):

        donation = donation_data.model_dump()

        async with uow:
            donation_id = await uow.donations.add_one(donation)
            await uow.commit()
            return donation_id

    async def get_info_donations_period(
            self,
            uow: IUnitOfWork,
            start_date: str,
            end_date: str,
    ):
        if start_date == end_date:
            raise ValueError("start_date and end_date cannot be the same")

        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()

        limit = 0
        async with uow:
            donation_start_list = await uow.donations.find_all(date=start_date_obj, page=0, limit=limit)
            donation_end_list = await uow.donations.find_all(date=end_date_obj, page=0, limit=limit)

            donations = donation_start_list + donation_end_list

            if len(donations) != 0:
                quantity_donation = len(donations)
                last_donation = max(donations, key=lambda donation: donation.date) if donations else None
            else:
                quantity_donation = 0
                last_donation = "Донаций за данный период не найдено"

            return {
                "quantity_donation": quantity_donation,
                "last_donation": last_donation,
            }

    async def get_all_donations(
            self,
            uow: IUnitOfWork,
            start_date: str,
            end_date: str,
            page: int,
            limit: int,
    ):
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()

        async with uow:
            donation_start_list = await uow.donations.find_all(date=start_date_obj, page=page, limit=limit)
            donation_end_list = await uow.donations.find_all(date=end_date_obj, page=page, limit=limit)

            donations = donation_start_list + donation_end_list

            return donations
