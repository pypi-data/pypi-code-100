import glob
import pathlib
from typing import Any, Dict, List, Set

from celery import Celery, Task, signature
from sqlalchemy import delete, select

from flowingo.configuration import conf
from flowingo.manager.app import app, logger
from flowingo.models import Pipeline, PipelineDump, PipelineTag, Session, Task, TaskGroup, TaskTag
from flowingo.pipelines import (
    get_pipeline_hash,
    get_pipeline_tasks_hash,
    read_pipeline,
    read_related_pipelines,
    validate_pipeline,
    validate_task,
)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls_collect_pipelines every 60 seconds.
    period = conf.manager_pipelines_refresh_period
    sender.add_periodic_task(period, refresh_all_pipelines.s(), name=f'refresh all pipelines every {period}')
    sender.add_periodic_task(period, refresh_all_tasks.s(), name=f'refresh all tasks every {period}')


def _save_pipelines_to_database(pipelines: Dict[str, Any], delete_missing: bool = False) -> None:
    """Update pipelines in database"""
    with Session.begin() as session:
        if delete_missing:
            _pipelines = session.execute(select(Pipeline)).scalars().all()
            for pipeline in list(_pipelines):
                if pipeline.filename not in pipelines:
                    session.delete(pipeline)
            session.flush()

        for current_filename, current_pipeline in pipelines.items():
            pipeline = session.execute(select(Pipeline).where(Pipeline.filename == current_filename)).scalar()

            if not pipeline:
                logger.info(f'Creating pipeline {pipeline}')
                pipeline = Pipeline(filename=current_filename)
                session.add(pipeline)
            else:
                logger.info(f'Updating pipeline {pipeline}')

            pipeline.ensure_up_to_date(session, current_pipeline)
            session.flush()


@app.task(bind=True, name='flowingo.refresh_pipeline', shared=False)
def refresh_pipeline(self: Task, filename: str) -> None:
    """Watch pipelines directory and list updated or new pipelines and it's status"""
    # read pipeline
    path = conf.pipelines_folder / filename
    assert path.exists(), f'Pipeline file {filename} must exists'

    # validate pipeline
    is_valid = validate_pipeline(conf.pipelines_folder, filename)

    if not is_valid:
        logger.warning(f'pipeline {filename} is not valid')
        raise Exception('pipeline must be valid')

    # read all related pipelines
    related_pipelines = read_related_pipelines(conf.pipelines_folder, filename)

    # Cache file in dumps and update main pipeline objects
    _save_pipelines_to_database(related_pipelines)


@app.task(bind=True, name='flowingo.refresh_all_pipelines', shared=False)
def refresh_all_pipelines(self: Task, validate_tasks: bool = False) -> None:
    """Watch pipelines directory and list updated or new pipelines and it's status"""

    # read all pipelines in pipeline dir
    pipeline_files = [
        str(i.relative_to(conf.pipelines_folder)) for i in conf.pipelines_folder.glob('*') if i.suffix in ['.yaml', '.yml']
    ]

    # validate all files
    invalid_pipelines: Set[str] = set()
    for filename in pipeline_files:
        # TODO: validate_tasks
        is_valid = validate_pipeline(conf.pipelines_folder, filename, tasks_folder=conf.tasks_folder if validate_tasks else None)

        if not is_valid:
            logger.warning(f'pipeline {filename} is not valid')
            logger.warning(f'pipeline {filename} will NOT be processed!')
            invalid_pipelines.add(filename)

    # read all valid pipelines
    pipelines = {f: read_pipeline(conf.pipelines_folder, f) for f in pipeline_files if f not in invalid_pipelines}

    # Cache file in dumps and update main pipeline objects
    _save_pipelines_to_database(pipelines, delete_missing=True)


def _save_tasks_to_database(group_tasks: Dict[str, Any]) -> None:
    with Session.begin() as session:
        groups = session.execute(select(TaskGroup)).scalars().all()

        # Delete deleted groups
        for group in list(groups):
            if group.filename not in group_tasks:
                session.delete(group)
        session.flush()

        # update all existed groups or create new
        for current_filename, current_group in group_tasks.items():
            # Update or create group
            group = session.execute(select(TaskGroup).where(TaskGroup.filename == current_filename)).scalar()
            if not group:
                logger.info(f'Creating group {group}')
                group = TaskGroup(filename=current_filename)
                session.add(group)
            else:
                logger.info(f'Updating group {group}')

            group.title = current_group.get('title', None)
            group.description = current_group.get('description', None)
            session.flush()

            # Delete tasks
            for task in list(group.tasks):
                if task.name not in current_group['tasks']:
                    group.tasks.remove(task)
                    # delete(task)
                    # session.delete(task)
                    # task.delete()
            session.flush()

            # Update tasks
            for task_name, task_desc in current_group['tasks'].items():
                task = session.execute(select(Task).where(Task.name == task_name)).scalar()

                if not task:
                    logger.info(f'Creating task {task}')
                    task = Task(name=task_name)
                    group.tasks.append(task)
                    # session.add(task)
                else:
                    logger.info(f'Updating task {task}')

                task.ensure_up_to_date(session, task_desc or {})
                task.group = group
            session.flush()


@app.task(bind=True, name='flowingo.refresh_all_tasks', shared=False)
def refresh_all_tasks(self: Task) -> None:
    """Watch tasks directory and list updated or new tasks and it's status"""

    # read all pipelines in pipeline dir
    tasks_files = [
        str(i.relative_to(conf.tasks_folder)) for i in conf.tasks_folder.glob('*') if i.suffix in ['.yaml', '.yml']
    ]

    # validate all files
    invalid_tasks_files: Set[str] = set()
    for filename in tasks_files:
        is_valid = validate_task(conf.tasks_folder, filename)

        if not is_valid:
            logger.warning(f'tasks file {filename} is not valid')
            logger.warning(f'tasks file {filename} will NOT be processed!')
            invalid_tasks_files.add(filename)

    # read all valid pipelines
    group_tasks = {f: read_pipeline(conf.tasks_folder, f) for f in tasks_files if f not in invalid_tasks_files}

    # Cache file in dumps and update main pipeline objects
    _save_tasks_to_database(group_tasks)
