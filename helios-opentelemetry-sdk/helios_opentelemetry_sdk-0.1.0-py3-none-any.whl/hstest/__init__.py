import os

import pytest
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

from helios import initialize

self_test = False
span_exporter = None
active_span = None
tracer_provider = None
tracer = None


def is_self_test(config):
    self_test_str = config.getoption('--self_test') or os.environ.get('HS_SELF_TEST', 'False')
    return self_test_str.lower() == "true"


def get_api_token(config):
    api_token = config.getoption('--hs_access_token') or os.environ.get('HS_ACCESS_TOKEN')
    if api_token is None:
        raise RuntimeError('Helios access token is missing.'
                           ' please set HS_ACCESS_TOKEN env var, '
                           ' or provide --hs_access_token argument to pytest command')
    return api_token


def pytest_configure(config):
    global span_exporter, tracer_provider, tracer, self_test
    service_name = config.getoption('--service_name')
    collector_endpoint = config.getoption('--collector_endpoint')
    environment = config.getoption('--environment')
    api_token = get_api_token(config)

    self_test = is_self_test(config)
    if self_test:
        span_exporter = InMemorySpanExporter()

    hs = initialize(
        api_token=api_token,
        service_name=service_name,
        collector_endpoint=collector_endpoint,
        environment=environment,
        enabled=True,
        span_exporter=span_exporter
    )

    tracer_provider = hs.get_tracer_provider()
    tracer = tracer_provider.get_tracer(__name__)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_protocol(item, nextitem):
    global active_span
    with tracer.start_as_current_span(item.name) as span:
        active_span = span
        # returns to test execution
        yield

    # When test is done
    active_span = None
    tracer_provider.force_flush()

    if self_test:
        run_self_test(item)


def run_self_test(item):
    expected_status = os.environ.get('HS_SELF_TEST_EXPECTED_STATUS', 'passed')
    child_span = None
    test_span = None
    child_span_name = os.environ.get('HS_SELF_TEST_EXPECTED_CHILD_SPAN')
    if span_exporter:
        for span in span_exporter.get_finished_spans():
            if span.attributes.get('otel.library.name') == child_span_name:
                child_span = span
            elif span.name == item.name:
                test_span = span

    assert test_span is not None

    assert test_span.attributes.get('test.name') == item.location[-1]
    assert test_span.attributes.get('test.status') == expected_status
    if expected_status == 'passed':
        assert test_span.attributes.get('test.error_message') == ''
    else:
        assert test_span.attributes.get('test.error_message') != ''

    if child_span_name:
        assert child_span is not None
        assert child_span.parent.span_id == test_span.context.span_id


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # returns to test execution
    outcome = yield

    # when test is done, extract the attributes from the test report
    result = outcome.get_result()
    if result.when == 'call':
        if active_span:
            active_span.set_attributes({
                'test.status': result.outcome,
                'test.name': result.head_line,
                'test.error_message': result.longreprtext,
            })


def pytest_addoption(parser):
    parser.addoption('--hs_access_token', help='access token for Helios', default=None)
    parser.addoption('--service_name', help='name of service under testing', default='unknown_service')
    parser.addoption('--collector_endpoint', help='OTEL collector endpoint', default='http://localhost:4317')
    parser.addoption('--environment', help='name of the environment where the tests are running', default=None)
    parser.addoption('--self_test', help='run tests in dry run mode', default=None)
