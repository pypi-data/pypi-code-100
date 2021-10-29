"""Script to create DB tables."""
from classes.stocks import Base
from classes.stocks import create_engine, sessionmaker


def create_tables():
    """Program entrypoint."""
    #engine = create_engine(conn_str)
    engine = create_engine('postgres://user:user@stock-data-postgres:5432/stocks')
    Session = sessionmaker(bind=engine)

    Base.metadata.create_all(engine)
    

"""
if __name__ == "__main__":

    conn_str = 'postgres://user:user@stock-data-postgres:5432/stocks'
    main(conn_str)
"""