import datetime
from typing import Any, Dict, List

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, select
from sqlalchemy.orm import relationship

from flowingo.models.base import Base, Session


class TaskGroup(Base):
    __tablename__ = 'task_group'

    id = Column(Integer, primary_key=True)
    filename = Column(String(128), unique=True, index=True)

    # Header
    title = Column(String(128), nullable=True, default=None)
    description = Column(Text, nullable=True, default=None)

    # relations
    tasks = relationship('Task', cascade='all,delete-orphan', back_populates='group')

    def __repr__(self):
        return f'<TaskGroup {self.id}: filename {self.filename}>'


class TaskTag(Base):
    __tablename__ = 'task_tag'

    name = Column(String(64), primary_key=True)
    task_id = Column(Integer, ForeignKey('task.id'), primary_key=True)

    # Relations
    task = relationship('Task', back_populates='tags')

    def __repr__(self) -> str:  # pragma: nocover
        return f'<Tag {self.name} for task_id: {self.task_id}>'


class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True, index=True)

    # Header
    title = Column(String(128))
    description = Column(Text)

    # Properties
    concurrency = Column(Integer, default=None, nullable=True)

    # Running info
    is_public = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)

    # Tech info
    group_id = Column(Integer, ForeignKey('task_group.id'))
    created_timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    updated_timestamp = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relations
    group = relationship('TaskGroup', foreign_keys=[group_id])
    # runs = relationship('TaskRun', cascade='all,delete-orphan', back_populates="task")  # TODO: runs for tasks
    tags = relationship('TaskTag', cascade='all,delete-orphan', back_populates="task")

    def ensure_up_to_date(self, session: Session, task: Dict[str, Any]) -> None:
        # Header
        if 'title' in task:
            self.title = task['title']
        if 'description' in task:
            self.description = task['description']

        # Properties
        if 'concurrency' in task:
            self.concurrency = task['concurrency']

        # Tags
        tags_names = list(set(task['tags'])) if 'tags' in task else []

        for tag in list(self.tags):
            if tag.name not in tags_names:
                self.tags.remove(tag)
                # session.delete(tag)

        for tag_name in tags_names:
            if tag_name not in [t.name for t in self.tags]:
                tag = TaskTag(name=tag_name, task_id=self.id)
                self.tags.append(tag)
                # session.add(tag)

        session.flush()

    def __repr__(self) -> str:  # pragma: nocover
        return f'<Task {self.id} {self.name}>'
