import datetime
from typing import Any, Optional

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, PickleType, String, Text
from sqlalchemy.orm import relationship

from flowingo.models.base import Base
from flowingo.models.pipelines import Pipeline
from flowingo.pipelines import get_pipeline_hash


class PipelineRun(Base):
    __tablename__ = 'pipeline_run'

    id = Column(Integer, primary_key=True)
    pipeline_id = Column(Integer, ForeignKey('pipeline.id', ondelete='CASCADE'), index=True)
    pipeline_dump_id = Column(Integer, ForeignKey('pipeline_dump.id'), nullable=True)
    author_id = Column(Integer, ForeignKey('user.id'))

    execution_timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    start_timestamp = Column(DateTime, nullable=True)
    end_timestamp = Column(DateTime, nullable=True)

    # Relations
    user = relationship('User')
    pipeline = relationship('Pipeline', back_populates='runs')

    def __repr__(self) -> str:  # pragma: nocover
        return f'<Run {self.id} for pipeline_id: {self.pipeline_id}>'
