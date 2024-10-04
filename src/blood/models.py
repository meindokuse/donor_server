from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship

from src.database import Base


class Donation(Base):

    __tablename__ = 'donation'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    group = Column(Integer)
    kell = Column(String, nullable=True)
    tromb = Column(String, nullable=True)
    plazma = Column(String, nullable=True)
    date = Column(TIMESTAMP, nullable=False)
    org = Column(String, nullable=False)

    user = relationship("User", back_populates="donations")

