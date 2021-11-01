import time
from typing import get_type_hints

from prometheus_client import Counter, Histogram, Summary, Info
from fastapi import Request


METRICS_REQUEST_LATENCY_HISTOGRAM = Histogram(
    "http_response_duration_ht_mss",
    "Duration of HTTP requests in ms (Histogram)",
    labelnames=["method", "route", "http_status"],
)

METRICS_REQUEST_LATENCY_SUMMARY = Summary(
    "http_response_duration_summary_mss",
    "Duration of HTTP requests in ms (Summary)",
    labelnames=["method", "route", "http_status"],
)

METRICS_REQUEST_COUNT = Counter(
    "http_request_totals",
    "Number of HTTP requests",
    labelnames=["method", "route", "http_status"],
)

METRICS_INFO = Info("app_versions", "Application Version")


def before_request():
    """
    Get start time of a request
    """
    Request._prometheus_metrics_request_start_time = time.time()


def inspect_request(response, request):

    method = request.method
    print(f"Request method: {method}\n")

    path = request.url.path
    print(f"Request path: {path}\n")

    status_code = response.status_code
    print(f"Request status_code: {status_code}\n")


def after_request(response, request):
    """
    Register Prometheus metrics after each request
    """
    request_latency = time.time() - request._prometheus_metrics_request_start_time
    METRICS_REQUEST_LATENCY_HISTOGRAM.labels(
        request.method, request.url.path, response.status_code
    ).observe(request_latency)
    METRICS_REQUEST_LATENCY_SUMMARY.labels(
        request.method, request.url.path, response.status_code
    ).observe(request_latency)
    METRICS_REQUEST_COUNT.labels(
        request.method, request.url.path, response.status_code
    ).inc()
    return response


def register_metrics(app):
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):

        print("__START MIDDLEWARE : ..")
        start_time = time.time()

        before_request()

        response = await call_next(request)

        inspect_request(response, request)
        after_request(response, request)

        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        print(str(process_time))
        print(str(response))
        print("__END MIDDLEWARE : ..\n")

        return response
