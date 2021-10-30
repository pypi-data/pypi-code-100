"""Script to create DB tables."""
from lbpackages.models.stocks import Base
from lbpackages.models.stocks import create_engine, sessionmaker
import os


def create_tables():
    """Program entrypoint."""
    #engine = create_engine(conn_str)
    print(os.getenv('USER'))
    engine = create_engine('postgresql://user:user@stock-data-postgres:5432/stocks')
    Session = sessionmaker(bind=engine)

    Base.metadata.create_all(engine)
    
    