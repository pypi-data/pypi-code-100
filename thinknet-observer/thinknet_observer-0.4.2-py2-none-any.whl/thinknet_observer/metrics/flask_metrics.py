import time

from flask import request
from prometheus_client import Counter, Histogram, Summary, Info

#
# Metrics registration
#


METRICS_REQUEST_LATENCY_HISTOGRAM = Histogram(
    "http_response_duration_ht_msf",
    "Duration of HTTP requests in ms (Histogram)",
    labelnames=["method", "route", "http_status"],
)

METRICS_REQUEST_LATENCY_SUMMARY = Summary(
    "http_response_duration_summary_msf",
    "Duration of HTTP requests in ms (Summary)",
    labelnames=["method", "route", "http_status"],
)

METRICS_REQUEST_COUNT = Counter(
    "http_request_totalf",
    "Number of HTTP requests",
    labelnames=["method", "route", "http_status"],
)

METRICS_INFO = Info("app_versionsss", "Application Version")


#
# Request callbacks
#


def before_request():
    """
    Get start time of a request
    """
    request._prometheus_metrics_request_start_time = time.time()


def after_request(response):
    """
    Register Prometheus metrics after each request
    """
    request_latency = time.time() - request._prometheus_metrics_request_start_time
    METRICS_REQUEST_LATENCY_HISTOGRAM.labels(
        request.method, request.path, response.status_code
    ).observe(request_latency)
    METRICS_REQUEST_LATENCY_SUMMARY.labels(
        request.method, request.path, response.status_code
    ).observe(request_latency)
    METRICS_REQUEST_COUNT.labels(
        request.method, request.path, response.status_code
    ).inc()
    return response


def register_metrics(app, app_version=None, app_config=None):
    """
    Register metrics middlewares
    Use in your application factory (i.e. create_app):
    register_middlewares(app, settings["version"], settings["config"])
    Flask application can register more than one before_request/after_request.
    Beware! Before/after request callback stored internally in a dictionary.
    Before CPython 3.6 dictionaries didn't guarantee keys order, so callbacks
    could be executed in arbitrary order.
    """
    app.before_request(before_request)
    app.after_request(after_request)
    METRICS_INFO.info({"version": app_version, "config": app_config})
