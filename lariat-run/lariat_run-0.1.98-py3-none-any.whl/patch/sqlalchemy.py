import sqlalchemy
from sqlalchemy.event import listen
from lariat.patch.statsd_config import DEFAULT_STATSD_CLIENT as Instrumentation

_create_engine = sqlalchemy.create_engine

def _before_cursor_execute(*args, **kwargs):
    statement, parameters = args[2], args[3]
    Instrumentation.event(
        Instrumentation.context.trace_id,
        "database.query",
        meta={
            "statement": statement,
            "parameters": parameters
        }
    )

def _patched_create_engine(url, **kwargs):
    engine = _create_engine(url, **kwargs)
    listen(engine, "before_cursor_execute", _before_cursor_execute)
    return engine

def patch():
    sqlalchemy.create_engine = _patched_create_engine
