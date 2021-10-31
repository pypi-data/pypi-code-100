import pathlib

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# TODO: create_async_engine, AsyncSession
path = pathlib.Path('.tmp/database/')
path.mkdir(parents=True, exist_ok=True)
DATABASE_URL = f"sqlite:///{path.absolute()}/sqlite.db"


engine = create_engine(
    DATABASE_URL, echo=False, future=True, connect_args={"check_same_thread": False}
)
Session = sessionmaker(engine, future=True)
# Session = sessionmaker(engine, future=True, expire_on_commit=False, class_=AsyncSession)


Base = declarative_base()


def init():
    # with engine.begin() as conn:
    #     conn.run_sync(Base.metadata.drop_all)
    # with engine.begin() as conn:
    #     conn.run_sync(Base.metadata.create_all)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def migrate():
    raise NotImplementedError()


def info():
    raise NotImplementedError()
