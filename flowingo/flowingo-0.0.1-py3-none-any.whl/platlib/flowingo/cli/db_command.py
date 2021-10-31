import click

from flowingo.models import info as info_db, init as init_db, migrate as migrate_db


@click.group()
def db():
    """db13 executable function"""
    pass


@db.command()
def migrate():
    """db13 executable function"""
    print('init db !!')
    migrate_db()


@db.command()
def init():
    """db13 executable function"""
    init_db()


@db.command()
def info():
    """db13 executable function"""
    print('info db !!')
    info_db()
