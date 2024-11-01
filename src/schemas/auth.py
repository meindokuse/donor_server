from datetime import date
from typing import Optional

from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    telegram_id: int
    group: int
    rezus: int
    kell: int

    class Config:
        orm_mode = True


class UserRead(BaseModel):
    id:int
    name: str
    telegram_id: int
    group: int
    rezus: int
    kell: int
    role_id: int
    registered_on: date

    class Config:
        orm_mode = True


class RegRequestCreate(BaseModel):
    name: str
    telegram_id: Optional[str]
    email: Optional[str]
    password: str


class RegRequestRead(BaseModel):
    id:int
    name: str
    telegram_id: Optional[str]
    email: Optional[str]
