from datetime import date
from typing import Optional

from pydantic import BaseModel


class DonationCreate(BaseModel):
    owner: str
    group: int
    kell: str
    tromb: Optional[str]
    plazma: Optional[str]
    rezus: Optional[int]
    org: str

class DonationRead(BaseModel):
    id:int
    owner: str
    group: int
    kell: str
    tromb: Optional[str]
    plazma: Optional[str]
    rezus: Optional[int]
    date: date
    org: str

