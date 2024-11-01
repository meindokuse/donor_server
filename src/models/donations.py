from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Date,Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import date
from src.db.database import Base
from src.schemas.auth import UserRead
from src.schemas.donations import DonationRead


class Donation(Base):
    __tablename__ = 'donation'

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(primary_key=True)
    owner: Mapped[str] = mapped_column(ForeignKey('users.name'))
    date: Mapped[date] = mapped_column(Date, nullable=False,default=date.today())
    org: Mapped[str] = mapped_column(nullable=False)
    is_free: Mapped[bool] = mapped_column(Boolean,nullable=False)

    user: Mapped["UserRead"] = relationship("Users", back_populates="donations")

    def to_read_model(self) -> "DonationRead":
        return DonationRead(
            id=self.id,
            type=self.type,
            owner=self.owner,
            date=self.date,
            org=self.org,
            is_free=self.is_free,
        )



