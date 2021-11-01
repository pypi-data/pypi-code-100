"""Data model definition to interact with the stocks DB."""

from sqlalchemy import Column, Date, Float, Integer, String, create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class StockValue(Base):
    """Stock value data model."""

    __tablename__ = "stock_value"
    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    date = Column(Date)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)

    def __init__(self, symbol, date, open, high, low, close):
        self.symbol = symbol
        self.date = date
        self.open = open
        self.high = high
        self.low = low
        self.close = close

    def __repr__(self):
        """Shows what the class is."""
        return f"<StockValue(symbol='{self.symbol}')>"
