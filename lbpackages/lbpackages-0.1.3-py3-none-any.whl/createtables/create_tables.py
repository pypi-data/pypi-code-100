"""Script to create DB tables."""
from lbpackages.models import stocks


def create_tables():
    """Program entrypoint."""
    #engine = create_engine(conn_str)
    engine = stocks.create_engine('postgres://user:user@stock-data-postgres:5432/stocks')
    Session = stocks.sessionmaker(bind=engine)

    stocks.Base.metadata.create_all(engine)
    

"""
if __name__ == "__main__":

    conn_str = 'postgres://user:user@stock-data-postgres:5432/stocks'
    main(conn_str)
"""