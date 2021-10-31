import random
import time

import celery
from celery import Task, signature
from celery.utils.log import get_task_logger

from flowingo.manager import celeryconfig

logger = get_task_logger(__name__)

app = celery.Celery(
    'manager',
    include=['flowingo.manager.tasks'],
    config_source=celeryconfig,
)


@app.task(bind=True, name='long_running_task')
def long_running_task(self: Task, context: dict) -> dict:
    logger.info(f'long_running_task')
    logger.info(f'context {context}')
    n = 100000
    total = 0
    for i in range(0, n):
        total += random.randint(1, 1000)
    time.sleep(5)
    context['long_running_task'] = total / n
    return context


@app.task(bind=True, name='sleep')
def sleep(self: Task, context: dict, duration=None):
    duration = int(duration) if duration else 0
    logger.info(f'sleep {sleep}')
    logger.info(f'context {context}')
    time.sleep(duration)
    return context


@app.task(bind=True, name='dummy')
def dummy(self: Task, context: dict) -> dict:
    logger.info(f'dummy')
    logger.info(f'context {context}')
    context['dummy'] = 'dummy'
    return context


@app.task(bind=True, name='setup')
def setup(self: Task, context: dict, key=None, value=None) -> dict:
    logger.info(f'set')
    logger.info(f'context {context}')
    context[key] = value
    return context




# task = app.send_task('flowingo._refresh_pipeline', args=['examples/pipelines/default.yml'], kwargs={})
# print(f'Started task: {task}')

task = app.send_task('flowingo.run_pipeline', args=[{'key': 'value'}], kwargs=dict(pipeline_id=1))
print(f'Started task: {task}')
