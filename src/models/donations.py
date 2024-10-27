from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Date
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import date
from src.db.database import Base
from src.schemas.auth import UserRead
from src.schemas.donations import DonationRead


class Donation(Base):
    __tablename__ = 'donation'

    id: Mapped[int] = mapped_column(primary_key=True)
    owner: Mapped[str] = mapped_column(ForeignKey('users.name'))
    group: Mapped[int] = mapped_column(nullable=False)
    kell: Mapped[str] = mapped_column(nullable=False)
    tromb: Mapped[str] = mapped_column(nullable=False)
    plazma: Mapped[str] = mapped_column(nullable=False)
    rezus: Mapped[int] = mapped_column(nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False,default=date.today())
    org: Mapped[str] = mapped_column(nullable=False)

    user: Mapped["UserRead"] = relationship("Users", back_populates="donations")

    def to_read_model(self) -> "DonationRead":
        return DonationRead(
            id=self.id,
            owner=self.owner,
            group=self.group,
            kell=self.kell,
            tromb=self.tromb,
            plazma=self.plazma,
            rezus=self.rezus,
            date=self.date,
            org=self.org
        )



