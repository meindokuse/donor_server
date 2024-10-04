from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DonationCreate:
    owner: int
    group: str
    tromb: Optional[str]
    plazma: Optional[str]
    rezus: Optional[str]
    date: datetime
    org: str

    class Config:
        orm_mode = True


class DonationGet(BaseModel):
    owner: int
    group: str
    tromb: Optional[str]
    plazma: Optional[str]
    rezus: Optional[str]
    date: datetime
    org: str

