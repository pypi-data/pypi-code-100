from logging import getLogger

from heliosphere.instrumentation.base import HeliosphereBaseInstrumentor
from heliosphere.instrumentation.botocore import HeliosphereBotocoreInstrumentor
from heliosphere.instrumentation.django import HeliosphereDjangoInstrumentor
from heliosphere.instrumentation.elasticsearch import HeliosphereElasticsearchInstrumentor
from heliosphere.instrumentation.fastapi import HeliosphereFastAPIInstrumentor
from heliosphere.instrumentation.flask import HeliosphereFlaskInstrumentor
from heliosphere.instrumentation.kafka import HeliosphereKafkaInstrumentor
from heliosphere.instrumentation.requests import HeliosphereRequestsInstrumentor
from heliosphere.instrumentation.urllib3 import HeliosphereUrllib3Instrumentor
from heliosphere.instrumentation.redis import HeliosphereRedisInstrumentor

_LOG = getLogger(__name__)

instrumentor_names = [
    ('opentelemetry.instrumentation.boto', 'BotoInstrumentor'),
    ('opentelemetry.instrumentation.celery', 'CeleryInstrumentor'),
    ('opentelemetry.instrumentation.mysql', 'MySQLInstrumentor'),
    ('opentelemetry.instrumentation.pymongo', 'PymongoInstrumentor'),
    ('opentelemetry.instrumentation.pymysql', 'PyMySQLInstrumentor'),
    ('opentelemetry.instrumentation.sqlalchemy', 'SQLAlchemyInstrumentor'),
    ('opentelemetry.instrumentation.urllib', 'URLLibInstrumentor'),
]

default_instrumentation_list = [
    HeliosphereBotocoreInstrumentor(),
    HeliosphereDjangoInstrumentor(),
    HeliosphereElasticsearchInstrumentor(),
    HeliosphereFastAPIInstrumentor(),
    HeliosphereFlaskInstrumentor(),
    HeliosphereKafkaInstrumentor(),
    HeliosphereRedisInstrumentor(),
    HeliosphereRequestsInstrumentor(),
    HeliosphereUrllib3Instrumentor(),
]

for module_name, instrumentor_name in instrumentor_names:
    instrumentor = HeliosphereBaseInstrumentor.init_instrumentor(module_name, instrumentor_name)
    if instrumentor is not None:
        default_instrumentation_list.append(instrumentor)
