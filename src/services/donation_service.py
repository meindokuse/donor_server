from datetime import datetime, timedelta

from mako.compat import win32
from sqlalchemy.sql.functions import current_date

from src.schemas.donations import DonationCreate
from src.data.unitofwork import IUnitOfWork

from src.utils import type_donations
from typing import Optional


class DonationService:

    async def get_donations_info_from_user(self, uow: IUnitOfWork, telegram_id: Optional[str] = None,
                                           name: Optional[str] = None):

        donations_info = {}

        status: int  # проверка для перерыва в донациях
        today_date = datetime.today().date()
        two_months_ago = today_date - timedelta(days=60)
        one_month_ago = today_date - timedelta(days=30)
        two_weeks_ago = today_date - timedelta(days=14)

        async with uow:

            if telegram_id:
                user = await uow.users.find_one(telegram_id=telegram_id)
                name = user.name
            else:
                user = await uow.users.find_one(name=name)
                name = user.name

            don = await uow.donations.find_all(page=1, limit=0, owner=name)
            if don == []:
                return None

            last_donation = max(don, key=lambda donation: donation.id)
            last_data = last_donation.date

            for t in type_donations:
                donations = await uow.donations.find_all(page=1, limit=0, owner=name, type=t)

                if donations:
                    quantity_donation = len(donations)

                    last_donation_type = max(donations, key=lambda donation: donation.id) if donations else None

                    if t == "Цельная кровь":
                        status = 1 if last_data <= two_months_ago else 0
                    if t in ["Плазма", "Тромбоциты"]:
                        status = 1 if last_data <= two_weeks_ago else 0
                    if t == "Гранулоциты":
                        status = 1 if last_data <= one_month_ago else 0

                    donations_info[t] = {"quantity_donation": quantity_donation, "last_donation": last_donation_type,
                                         "status": status}

            return donations_info

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

            return {'donations': donations, 'quantity_donation': len(donations)}

    async def add_donation(self, uow: IUnitOfWork, donation_data: DonationCreate):

        donation = donation_data.model_dump()

        async with uow:
            donation_id = await uow.donations.add_one(donation)
            await uow.commit()
            return donation_id

    async def get_all_donations(
            self,
            uow: IUnitOfWork,
            start_date: str,
            end_date: str,
            page: int,
            limit: int,
            type_donation: Optional[str] = None,
    ):

        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()

        async with uow:
            donations_t_list = await uow.donations.get_donations_by_date(start_date=start_date_obj,
                                                                         end_date=end_date_obj, page=page, limit=limit)

            all_donations = await uow.donations.get_donations_by_date(start_date=start_date_obj,
                                                                      end_date=end_date_obj, page=page, limit=0)

            quantity_donation = len(all_donations)

            return {
                "quantity_donation": quantity_donation,
                "donations": donations_t_list
            }

    async def get_table_donations(self, uow: IUnitOfWork):
        async with uow:
            rows = await uow.donations.get_table()

            return rows
