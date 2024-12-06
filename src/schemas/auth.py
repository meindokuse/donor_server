from datetime import date
from typing import Optional

from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    telegram_id: str
    group: int
    rezus: bool
    kell: bool

    class Config:
        orm_mode = True


class UserRead(BaseModel):
    id:int
    name: str
    telegram_id: str
    group: int
    rezus: bool
    kell: bool
    role_id: int
    registered_on: date
    status: float

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
