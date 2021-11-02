#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlalchemy.orm
import sqlalchemy.engine.url
import contextlib
import collections


class Helper:
    def __init__(self):
        self._engines = collections.defaultdict(dict)

    @property
    def pid(self):
        import os
        return os.getpid()

    def _create(self, name: str):
        parts = name.split(":")
        key, rw = parts if len(parts) == 2 else (name, "read")

        from ._config import get as get_config
        conf = get_config("database", key)  # type: dict
        assert conf, f"Database configuration not exists: {name}"
        if rw in conf:
            conf = conf[rw]

        e = sqlalchemy.create_engine(
            sqlalchemy.engine.url.URL(
                drivername="mysql+pymysql",
                username=conf["user"],
                password=conf["password"],
                host=conf["host"],
                port=conf["port"],
                database=conf["database"]
            ),
            pool_pre_ping=True
        )
        self._engines[self.pid][name] = e
        return e

    def _get(self, name):
        e = self._engines[self.pid].get(name)
        if e is None:
            e = self._create(name)
        return e

    @contextlib.contextmanager
    def session(self, name) -> sqlalchemy.orm.Session:
        e = self._get(name)
        session = sqlalchemy.orm.Session(bind=e, autocommit=False)
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    @contextlib.contextmanager
    def __call__(self, name) -> sqlalchemy.engine.Connection:
        with self.engine(name).connect() as con:
            yield con

    def engine(self, name) -> sqlalchemy.engine.Engine:
        return self._get(name)


helper = Helper()
