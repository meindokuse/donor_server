from datetime import date

from pydantic import BaseModel


class DonationCreate(BaseModel):
    owner: str
    type: str
    is_free: bool
    org: str


class DonationRead(BaseModel):
    id: int
    type: str
    owner: str
    is_free: bool
    date: date
    org: str
