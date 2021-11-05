from sqlalchemy import (  # noqa: F401
    JSON,
    BigInteger,
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy import create_engine as _create_engine
from sqlalchemy import desc, func  # noqa: F401
from sqlalchemy.exc import IntegrityError  # noqa: F401
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (  # noqa: F401
    Session,
    declarative_mixin,
    joinedload,
    load_only,
    relationship,
    sessionmaker,
)

from initcommerce.common.logger import get_logger
from initcommerce.common.uuid import UUID

logger = get_logger("initcommerce-utils")

# HACK: enforce singleton
_conn: Session = None


def get_db(db_uri: str):
    global _conn

    engine = _create_engine(db_uri, pool_pre_ping=True)

    if _conn is None:
        SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine,
        )
        _conn = SessionLocal()

    if not _conn.is_active:
        _conn.rollback()
        logger.error("Connection rollback occurred!")

    return _conn


BaseDBModel = declarative_base()


@declarative_mixin
class PrimaryIDMixin:
    id = Column(
        BigInteger, primary_key=True, autoincrement=False, default=UUID.fetch_one
    )


@declarative_mixin
class IndexedIDMixin:
    id = Column(BigInteger, index=True, default=UUID.fetch_one)
