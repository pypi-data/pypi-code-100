import pickle
import logging
from typing import Optional
from functools import partial
import sqlalchemy
import psycopg2

logger = logging.getLogger(__name__)

def get_metadata(engine):
    metadata = sqlalchemy.MetaData()
    metadata.reflect(engine)
    logger.info(f"Got metadata! ({len(metadata.tables)} tables)")
    return metadata

def set_metadata(engine, metadata: sqlalchemy.MetaData, replace = False):
    existing_metadata = sqlalchemy.MetaData()
    existing_metadata.reflect(bind = engine)

    if replace:
        logger.warning(f"Dropping existing tables!! ({len(existing_metadata.tables)} tables)")
        existing_metadata.drop_all(bind = engine)
    elif (n_tables := len(existing_metadata.tables)) > 0:
        raise ValueError(f"Database already has metadata ({n_tables} tables)")

    logger.info("Read metadata")
    metadata.create_all(bind = engine)
    logger.info("Added new metadata")

def constr(
        host: str,
        port: int,
        user: str,
        password: Optional[str],
        dbname: str,
        sslmode: str):
    cs = (
            f"host={host} "
            f"port={port} "
            f"user={user} "
            f"password={password} "
            f"dbname={dbname} "
            f"sslmode={sslmode} "
        )
    if password:
        cs += f"password={password} "

    return cs

def creator(host, port, user, password, dbname, sslmode):
    return psycopg2.connect(constr(host,port,user,password,dbname,sslmode))

def create_engine(host, port, user, password, dbname, sslmode):
    return sqlalchemy.create_engine("postgresql://", creator = partial(creator,host,port,user,password,dbname,sslmode))
