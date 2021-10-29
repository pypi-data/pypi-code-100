from datetime import datetime
from sqlalchemy import CHAR, Column, DateTime, Float, Index, String, Text, text, ForeignKey, \
    UniqueConstraint, PrimaryKeyConstraint, DECIMAL
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.sql import func


class CommonField(object):
    """ warning: nullable default=False, 只定义为True的那些"""
    __abstract__ = True

    createdAt = Column(DateTime, default=datetime.now)
    updatedAt = Column(DateTime, default=datetime.now)
    id = Column(INTEGER(64), primary_key=True, autoincrement=False)
    tenant_id = Column(String(32))
    created_at = Column(DateTime, nullable=False, default=datetime.now, server_default=func.now(), comment='创建时间')
    created_pin = Column(String(32))
    updated_at = Column(DateTime, nullable=False, default=datetime.now, server_default=func.now(), comment='更新时间')
    updated_pin = Column(String(32))
    version = Column(INTEGER(32), default=0, server_default=0)
    iz_del = Column(TINYINT(1), default=0, server_default=0, comment='逻辑删除')
