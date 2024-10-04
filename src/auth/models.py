from sqlalchemy import Column, String, Integer, TIMESTAMP, ForeignKey, JSON, ARRAY
from sqlalchemy.orm import relationship

from src.database import Base
from datetime import datetime


class Achievement(Base):
    __tablename__ = 'achievement'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    get_at = Column(TIMESTAMP, default=datetime.utcnow)


class Roles(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    permissions = Column(JSON)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(String(50), unique=True, nullable=True)
    name = Column(String(50))
    email = Column(String(50), unique=True, nullable=True)  # Уникальность email
    password = Column(String(50))
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    role_id = Column(Integer, ForeignKey('roles.id'))
    donations = relationship("Donation", back_populates="user")


class RegRequest(Base):
    __tablename__ = 'reg_request'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(String(50), unique=True, nullable=True)
    name = Column(String(50))
    email = Column(String(50), unique=True, nullable=True)  # Уникальность email
    password = Column(String(50))


