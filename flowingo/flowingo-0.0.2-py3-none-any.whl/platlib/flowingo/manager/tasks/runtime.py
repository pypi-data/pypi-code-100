import datetime
from typing import Any, Dict, List, Optional

from celery import Celery, Task, signature
from celery.canvas import Signature, chain, chord, group
from sqlalchemy import select

from flowingo.manager.app import app, logger
from flowingo.models import Pipeline, PipelineRun, Session


@app.task(bind=True, name='flowingo.task.merge_context', shared=False)
def merge_context_task(self: Task, contexts: List[Dict[str, Any]]) -> Dict[str, Any]:
    context = {}
    for i in contexts:
        if i:
            context.update(i)
    return context


def _get_common_task(task_config: Dict[str, Any]) -> Signature:
    task_name = task_config['task']
    parameters = task_config['parameters'] if 'parameters' in task_config else {}
    task_sign = signature(task_name, kwargs=parameters)

    return task_sign


def _get_task(task_config: Dict[str, Any]) -> Signature:
    if 'group' in task_config:
        return _get_group_task(task_config['group'])

    if 'chain' in task_config:
        return _get_chain_task(task_config['chain'])

    if 'if' in task_config:
        return _get_if_task(task_config)

    return _get_common_task(task_config)


def _get_group_task(tasks_configs: List[Dict[str, Any]]) -> Signature:
    tasks = []
    for task_config in tasks_configs:
        task_sign = _get_task(task_config)
        tasks.append(task_sign)

    chord_tasks_signature = chord(tasks, merge_context_task.s())
    # chord_tasks_signature = group(tasks) | merge_context_task.s()

    return chord_tasks_signature


def _get_chain_task(tasks_configs: List[Dict[str, Any]]) -> Signature:
    if isinstance(tasks_configs, str):
        raise NotImplementedError
        # tasks_configs = _read_yml(tasks_configs)

    tasks = []
    for task_config in tasks_configs:
        task_sign = _get_task(task_config)
        tasks.append(task_sign)

    chain_tasks_signature = chain(*tasks)

    return chain_tasks_signature


@app.task(bind=True, name='flowingo.task.if', shared=False)
def if_task(self: Task, context: Dict[str, Any], key=None, values=None) -> Dict[str, Any]:
    if key not in context:
        return context

    value = context[key]
    tasks_to_run = values.get(value, None) or values.get('default', None)

    if not tasks_to_run:
        return context

    if isinstance(tasks_to_run, str):
        tasks_signature = start_pipeline_run_task.s(pipeline_filename=tasks_to_run)
    elif isinstance(tasks_to_run, list):
        tasks_signature = _get_chain_task(tasks_to_run)
    else:
        raise RuntimeError(f'Unknown type of value {type(tasks_to_run)} of {tasks_to_run}')

    tasks_signature = tasks_signature.replace(args=(context,))
    return self.replace(tasks_signature)


def _get_if_task(tasks_config: dict) -> Signature:
    key = tasks_config['if']
    values = tasks_config['values']

    return if_task.s(kwargs=dict(key=key, values=values))


@app.task(bind=True, name='flowingo.task.sub_pipeline', shared=False)
def run_sub_pipeline_task(self: Task, context: Dict[str, Any], pipeline_id: Optional[int] = None, pipeline_filename: Optional[str] = None) -> Dict[str, Any]:
    with Session.begin() as session:
        if pipeline_id is not None:
            pipeline = session.get(Pipeline, pipeline_id)
        elif pipeline_filename is not None:
            pipeline = session.execute(select(Pipeline).where(Pipeline.filename == pipeline_filename)).scalar()
        else:
            raise RuntimeError('pipeline_id or pipeline_filename should be provided')

        if not pipeline:
            raise RuntimeError('pipeline_id must exist in database')

        tasks = pipeline.tasks

    chain_task_signature = _get_chain_task(tasks)
    chain_task_signature = chain_task_signature.replace(args=(context,))
    return self.replace(chain_task_signature)


@app.task(bind=True, name='flowingo.task.start_pipeline_run', shared=False)
def start_pipeline_run_task(self: Task, context: Dict[str, Any], *args, pipeline_id: Optional[int] = None, run_id: Optional[int] = None) -> Dict[str, Any]:
    logger.info(f'Started pipeline {pipeline_id} with run {run_id}')

    with Session.begin() as session:
        pipeline_run = session.get(PipelineRun, run_id)

        if not pipeline_run:
            raise RuntimeError('run_id must exist in database')

        pipeline_run.start_timestamp = datetime.datetime.utcnow()

    return context


@app.task(bind=True, name='flowingo.task.end_pipeline_run', shared=False)
def end_pipeline_run_task(self: Task, context: Dict[str, Any], pipeline_id: Optional[int] = None, run_id: Optional[int] = None) -> Dict[str, Any]:
    logger.info(f'Ending pipeline {pipeline_id} with run {run_id}')

    with Session.begin() as session:
        pipeline_run = session.get(PipelineRun, run_id)

        if not pipeline_run:
            raise RuntimeError('run_id must exist in database')

        pipeline_run.end_timestamp = datetime.datetime.utcnow()

        # TODO: save output

    return context


@app.task(bind=True, name='flowingo.run_pipeline')
def run_pipeline(self: Task, context: Dict[str, Any], pipeline_id: Optional[int] = None) -> Dict[str, Any]:
    logger.info(f'run_pipeline {pipeline_id}')

    if not pipeline_id:
        raise RuntimeError('pipeline_id can not be None')

    context = context or {}

    with Session.begin() as session:
        pipeline = session.get(Pipeline, pipeline_id)

        if not pipeline:
            raise RuntimeError('pipeline_id must exist in database')
        if not pipeline.sub:
            raise RuntimeError('Can not run sub pipeline')

        tasks = pipeline.tasks

        pipeline_run = PipelineRun(pipeline_id=pipeline.id, pipeline_dump_id=pipeline.dump_id)
        session.add(pipeline_run)
        session.flush()
        run_id = pipeline_run.id

    logger.info(f'run_pipeline tasks {tasks}')

    chain_task_signature = _get_chain_task(tasks)
    logger.info(f'run_pipeline tasks {chain_task_signature} args {chain_task_signature.args}')

    _run_pipeline_tasks = chain(
        start_pipeline_run_task.s(pipeline_id=pipeline_id, run_id=run_id),
        chain_task_signature,
        end_pipeline_run_task.s(pipeline_id=pipeline_id, run_id=run_id),
    )

    _run_pipeline_tasks = _run_pipeline_tasks.replace(args=(context,))
    logger.info(f'run_pipeline tasks {_run_pipeline_tasks} args {_run_pipeline_tasks.args}')

    return self.replace(_run_pipeline_tasks)
