from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    telegram_id: Optional[str]
    email: Optional[str]
    password: str

    class Config:
        orm_mode = True


class UserRead(BaseModel):
    name: str
    telegram_id: Optional[str]
    email: str
    role_id: int
    registered_on: datetime

    class Config:
        orm_mode = True


class RegRequestCreate(BaseModel):
    username: str
    telegram_id: Optional[str]
    email: Optional[str]
    password: str


class RegRequestRead(BaseModel):
    username: str
    email: Optional[str]
    password: Optional[str]
    registered_on: datetime
