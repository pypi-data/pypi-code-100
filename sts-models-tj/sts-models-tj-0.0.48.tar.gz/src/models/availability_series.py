from . import Base
from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship


class AvailabilitySeries(Base):
    """Availability Series Model for connecting availabilities made as a repeating series"""
    __tablename__ = "availability_series"

    id = Column(Integer, primary_key=True, autoincrement=True)
    availabilities = relationship("Availability", cascade="all, delete, delete-orphan")
