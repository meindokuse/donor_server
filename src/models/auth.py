
from sqlalchemy import Column, String, Integer, Date, Boolean, FLOAT, NUMERIC
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.db.database import Base
from datetime import date

from src.schemas.auth import RegRequestRead
from src.schemas.auth import UserRead
from src.schemas.donations import DonationRead


class Achievement(Base):
    __tablename__ = 'achievement'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    owner = Column(String, nullable=False)
    get_at = Column(Date, default=date.today)


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    telegram_id: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    group: Mapped[int] = mapped_column(Integer, nullable=False)
    kell: Mapped[bool] = mapped_column(Boolean, nullable=False)
    rezus: Mapped[bool] = mapped_column(Boolean, nullable=False)
    registered_at: Mapped[date] = mapped_column(Date, default=date.today)
    role_id: Mapped[int] = mapped_column(Integer, nullable=False, default=2)
    status: Mapped[float] = mapped_column(NUMERIC(4, 2), nullable=False, default="Начинающий донор")

    donations: Mapped[list["DonationRead"]] = relationship("Donation", back_populates="user")

    def to_read_model(self) -> "UserRead":
        return UserRead(
            id=self.id,
            name=self.name,
            group=self.group,
            rezus=self.rezus,
            kell=self.kell,
            telegram_id=self.telegram_id,
            role_id=self.role_id,
            registered_on=self.registered_at,
            status=self.status,
        )


class RegRequest(Base):
    __tablename__ = 'reg_request'

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    password: Mapped[str] = mapped_column(String(255), unique=True)

    def to_read_model(self) -> "RegRequestRead":
        return RegRequestRead(
            id=self.id,
            telegram_id=self.telegram_id,
            name=self.name,
            email=self.email
        )
