import logging
import os
import sys
from pathlib import Path

from celery import Celery
from celery.signals import after_setup_logger, after_setup_task_logger
from kombu import Exchange, Queue

# from celery.utils.log import get_task_logger


""" ========== Logger settings ========== """


@after_setup_logger.connect
@after_setup_task_logger.connect
def setup_loggers(logger, *args, **kwargs):
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # FileHandler
    fh = logging.FileHandler('.tmp/celery/logs.log')
    # fh.setFormatter(formatter)
    logger.addHandler(fh)

    # SysLogHandler
    slh = logging.handlers.SysLogHandler(address=('logsN.papertrailapp.com', '...'))
    # slh.setFormatter(formatter)
    logger.addHandler(slh)


""" ========== Backend and broker ========== """

broker_url = os.getenv('CELERY_BROKER_URL', 'filesystem://')
backend_url = os.getenv('CELERY_BACKEND_URL', 'file://')

_broker_folder = None
broker_transport_options = {}
if broker_url == 'filesystem://':
    _broker_folder = os.getenv('CELERY_BROKER_FOLDER', '.tmp/celery/broker')
    for f in ['in', 'processed']:
        if not os.path.exists(os.path.join(_broker_folder, f)):
            os.makedirs(os.path.join(_broker_folder, f))
    broker_transport_options = {
        'data_folder_in': os.path.join(_broker_folder, 'in'),
        'data_folder_out': os.path.join(_broker_folder, 'in'),
        'data_folder_processed': os.path.join(_broker_folder, 'processed')
    }

_backend_folder = None
result_backend = None
if backend_url == 'file://':
    _backend_folder = os.getenv('CELERY_BROKER_FOLDER', '.tmp/celery/results')
    if not os.path.exists(_backend_folder):
        os.makedirs(_backend_folder)
    result_backend = os.path.join(backend_url, _backend_folder)


""" ========== General settings ========== """

result_persistent = True
task_track_started = True  # Not only PENDING state, but also STARTED
worker_send_task_events = True

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json', 'msgpack']


""" ========== Tasks settings ========== """

task_time_limit = 60
task_soft_time_limit = 60


""" ========== Queues settings ========== """

task_default_priority = 5

task_queues = (
    Queue('manager', Exchange('manager'), routing_key='manager'),
    Queue('manager.pipelines',  Exchange('manager'),   routing_key='manager.pipelines'),
    Queue('manager.runtime',  Exchange('manager'),   routing_key='manager.runtime'),
)
task_default_queue = 'manager'
task_default_exchange_type = 'direct'
task_default_routing_key = 'manager'
