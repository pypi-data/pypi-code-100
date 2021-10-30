"""Script to create DB tables."""
from lbpackages.models.stocks import Base
from lbpackages.models.stocks import create_engine, sessionmaker
import os

USER = os.getenv('STOCKS_USER')
PASS = os.getenv('STOCKS_PASS')

def create_tables(USER=USER, PASS=PASS):
    """Program entrypoint."""
    engine = create_engine(f'postgresql://{USER}:{PASS}@stock-data-postgres:5432/stocks')
    Session = sessionmaker(bind=engine)

    Base.metadata.create_all(engine)
    
    