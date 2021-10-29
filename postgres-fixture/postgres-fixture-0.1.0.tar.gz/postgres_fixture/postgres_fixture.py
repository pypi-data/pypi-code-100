
import json
from contextlib import closing
import logging
from typing import Optional
from io import BufferedWriter, BufferedReader
import pickle
import click
import sqlalchemy
from . import db, analysis 

logger = logging.getLogger(__name__)

def load_metadata(file: BufferedReader) -> sqlalchemy.MetaData:
    md = pickle.load(file)
    assert isinstance(md,sqlalchemy.MetaData)
    return md


@click.group()
@click.option("--debug/--no-debug", type = bool, default = False)
def postgres_fixture(debug: bool):
    lvl = logging.WARNING if not debug else logging.DEBUG
    logging.basicConfig(level = lvl)

@postgres_fixture.command()
@click.option("-h","--host", type = str, default = "0.0.0.0")
@click.option("-p","--port", type = int, default = 5432)
@click.option("-U","--user", type = str, default = "postgres")
@click.option("-W","--password", type = str, default = None)
@click.option("-d","--dbname", type = str, default = "postgres")
@click.option("-s","--sslmode", type = str, default = "allow")
@click.argument("outfile", type = click.File("wb"))
def get_metadata(
        host: str,
        port: int,
        user: str,
        password: Optional[str],
        dbname: str,
        sslmode: str,
        outfile: BufferedWriter):

    engine = db.create_engine(host,port, user, password, dbname, sslmode)
    logger.info("Successfully connected to DB")
    metadata = db.get_metadata(engine)
    logger.info("Writing to file")
    pickle.dump(metadata, outfile)

@postgres_fixture.command()
@click.option("-h","--host", type = str, default = "0.0.0.0")
@click.option("-p","--port", type = int, default = 5432)
@click.option("-U","--user", type = str, default = "postgres")
@click.option("-W","--password", type = str, default = None)
@click.option("-d","--dbname", type = str, default = "postgres")
@click.option("-s","--sslmode", type = str, default = "allow")
@click.option("--replace/--no-replace", type = bool, default = False)
@click.argument("infile", type = click.File("rb"))
def set_metadata(
        host: str,
        port: int,
        user: str,
        password: Optional[str],
        dbname: str,
        sslmode: str,
        infile: BufferedReader,
        replace: bool):


    engine = db.create_engine(host,port, user, password, dbname, sslmode)
    logger.info("Successfully connected to DB")
    metadata = pickle.load(infile)
    assert isinstance(metadata, sqlalchemy.MetaData)
    logger.info("Read metadata")
    db.set_metadata(engine, metadata, replace)

@postgres_fixture.command()
@click.option("-h","--host", type = str, default = "0.0.0.0")
@click.option("-p","--port", type = int, default = 5432)
@click.option("-U","--user", type = str, default = "postgres")
@click.option("-W","--password", type = str, default = None)
@click.option("-d","--dbname", type = str, default = "postgres")
@click.option("-s","--sslmode", type = str, default = "allow")
@click.option("--cached-metadata", type = click.File("rb"), default = None)
def get_counts(
        host: str,
        port: int,
        user: str,
        password: Optional[str],
        dbname: str,
        sslmode: str,
        cached_metadata: Optional[BufferedReader]):

    engine = db.create_engine(host,port, user, password, dbname, sslmode)
    logger.info("Successfully connected to DB")

    if cached_metadata is not None:
        logger.info("Loading metadata from file")
        metadata = load_metadata(cached_metadata)
    else:
        logger.info("Reflecting metadata...")
        metadata = sqlalchemy.MetaData()
        metadata.reflect(bind = engine)

    with closing(engine.connect()) as conn:
        click.echo(json.dumps(analysis.counts(conn, metadata)))
