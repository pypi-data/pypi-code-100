import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, PickleType, String, Text, delete, select
from sqlalchemy.orm import relationship

from flowingo.models.base import Base, Session
from flowingo.pipelines import get_pipeline_hash


class PipelineTag(Base):
    __tablename__ = 'pipeline_tag'

    name = Column(String(64), primary_key=True)
    pipeline_id = Column(Integer, ForeignKey('pipeline.id', ondelete='CASCADE'), primary_key=True)

    # Relations
    pipeline = relationship('Pipeline', back_populates='tags')

    def __repr__(self) -> str:  # pragma: nocover
        return f'<Tag {self.name} for pipeline_id: {self.pipeline_id}>'


class PipelineDump(Base):
    __tablename__ = 'pipeline_dump'

    id = Column(Integer, primary_key=True)
    pipeline_id = Column(Integer, ForeignKey('pipeline.id', ondelete='CASCADE'), index=True)

    pipeline_pickle = Column(PickleType())
    pipeline_hash = Column(String(64), index=True)

    created_timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    # Relations
    pipeline = relationship('Pipeline', foreign_keys=[pipeline_id])

    def __init__(self, pipeline_dict: Optional[dict] = None, *args, **kwargs):
        super(PipelineDump, self).__init__(*args, **kwargs)
        if pipeline_dict:
            self.pipeline_hash = get_pipeline_hash(pipeline_dict)
            self.pipeline_pickle = pipeline_dict

    def __repr__(self) -> str:  # pragma: nocover
        return f'<PipelineDump {self.id}: pipeline_id {self.pipeline_id}>'


class Pipeline(Base):
    __tablename__ = 'pipeline'

    id = Column(Integer, primary_key=True)  # TODO: uuid
    filename = Column(String(128), unique=True, index=True)

    # Header
    title = Column(String(128))
    description = Column(Text, nullable=True, default=None)

    # Properties
    sub = Column(Boolean, default=False)
    concurrency = Column(Integer, nullable=True, default=None)

    # Running info
    is_public = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)

    # Tech info
    dump_id = Column(Integer, ForeignKey('pipeline_dump.id'))
    created_timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    updated_timestamp = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    author_id = Column(Integer, ForeignKey('user.id'), nullable=True)

    # Relations
    author = relationship('User')
    runs = relationship('PipelineRun', cascade='all,delete,delete-orphan', back_populates='pipeline')
    tags = relationship('PipelineTag', cascade='all,delete,delete-orphan', back_populates='pipeline')
    dump = relationship('PipelineDump', foreign_keys=[dump_id], uselist=False, post_update=True)
    dumps = relationship('PipelineDump', foreign_keys=[PipelineDump.pipeline_id], cascade='all,delete,delete-orphan', back_populates='pipeline')

    # def __init__(self, pipeline: Optional[dict] = None, *args: Any, **kwargs: Any):
    #     super(Pipeline, self).__init__(*args, **kwargs)
    #     if pipeline:
    #         self.ensure_up_to_date(self, pipeline)

    def ensure_up_to_date(self, session: Session, pipeline: Dict[str, Any]) -> None:
        # Header
        self.title = pipeline['title']
        if 'description' in pipeline:
            self.description = pipeline['description']

        # Properties
        if 'properties' in pipeline:
            properties = pipeline['properties']
            if 'sub' in properties:
                self.sub = properties['sub']
            if 'concurrency' in properties:
                self.concurrency = properties['concurrency']

        # Tags
        tags_names = list(set(pipeline['tags'])) if 'tags' in pipeline else []

        for tag in list(self.tags):
            if tag.name not in tags_names:
                self.tags.remove(tag)
                # session.delete(tag)

        for tag_name in tags_names:
            if tag_name not in [t.name for t in self.tags]:
                tag = PipelineTag(name=tag_name, pipeline_id=self.id)
                self.tags.append(tag)
                # session.add(tag)

        # Dump
        pipeline_hash = get_pipeline_hash(pipeline)

        pipeline_dump = session.execute(
            select(PipelineDump)
            .where(PipelineDump.pipeline_id == self.id)
            .where(PipelineDump.pipeline_hash == pipeline_hash)
        ).scalar()

        # Exists exactly hashed pipeline.
        if pipeline_dump:
            self.dump_id = pipeline_dump.id  # Ensure dump linked and exit
        else:
            # Create pipeline dump
            pipeline_dump = PipelineDump(pipeline_pickle=pipeline, pipeline_hash=pipeline_hash, pipeline_id=self.id)
            self.dump = pipeline_dump
            session.add(pipeline_dump)

        session.flush()

    @property
    def tasks(self) -> List[Dict[str, Any]]:
        return self.dump.pipeline_pickle['tasks']

    @property
    def pipeline(self) -> Dict[str, Any]:
        return self.dump.pipeline_pickle

    def __repr__(self) -> str:  # pragma: nocover
        return f'<Pipeline: {self.id}: title: {self.title}>'

