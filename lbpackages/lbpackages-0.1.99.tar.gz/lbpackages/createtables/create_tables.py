"""Script to create DB tables."""
from lbpackages.models.stocks import Base
from lbpackages.models.stocks import create_engine, sessionmaker
import os



def create_tables():
    """Program entrypoint."""
    USER = str(os.getenv('STOCKS_USER'))
    PASS = str(os.getenv('STOCKS_PASS'))
    print(f'postgresql://{USER}:{PASS}@stock-data-postgres:5432/stocks')
    engine = create_engine(f'postgresql://{USER}:{PASS}@stock-data-postgres:5432/stocks')
    Session = sessionmaker(bind=engine)

    Base.metadata.create_all(engine)
    
    