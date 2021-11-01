import time
import fastapi

from flask import Flask
from flask import request as flask_request
from fastapi import FastAPI
from fastapi import Request as fastapi_request
from fastapi.middleware.wsgi import WSGIMiddleware

from prometheus_client import Counter, Histogram, Summary, Info
from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware


class Metric:
    def __init__(self, app) -> None:
        """
        :param app: web application framework can be either 'Flask' or 'fastapi'.
        :type app: 'astapi.applications.FastAPI' or 'flask.app.Flask'

        """
        self._app = None
        self._app_type = ""
        self.request = None
        self.exclude_route = []

        self.METRICS_REQUEST_LATENCY_HISTOGRAM = Histogram(
            "http_response_duration_ht_ms",
            "Duration of HTTP requests in ms (Histogram)",
            labelnames=["method", "route", "http_status"],
        )

        self.METRICS_REQUEST_LATENCY_SUMMARY = Summary(
            "http_response_duration_summary_ms",
            "Duration of HTTP requests in ms (Summary)",
            labelnames=["method", "route", "http_status"],
        )

        self.METRICS_REQUEST_COUNT = Counter(
            "http_request_total",
            "Number of HTTP requests",
            labelnames=["method", "route", "http_status"],
        )

        self.METRICS_INFO = Info("app_version", "Application Version")

        self.set_app(app)

    def app(self):
        return self._app

    def set_app(self, new_app):
        if isinstance(new_app, Flask):
            self._app = new_app
            self.request = flask_request
            print(self.request)
        elif isinstance(new_app, FastAPI):
            self._app = new_app
            self.request = fastapi_request
            print(self.request)

        else:
            raise TypeError("app type have to be etiher 'Flask' or 'fastapi'.")

    def register_metrics(self, app_version=None, app_config=None):
        # self.add_middleware(app_version, app_config)
        if isinstance(self._app, Flask):
            self.add_flask_middleware()
        elif isinstance(self._app, FastAPI):
            self.add_fastapi_middleware()

    # def add_middleware(self, app_version=None, app_config=None):
    #     if isinstance(self._app, Flask):
    #         self._app.wsgi_app = DispatcherMiddleware(
    #             self._app.wsgi_app, {"/metrics": make_wsgi_app()}
    #         )
    #         """
    #         Register metrics middlewares
    #         Use in your application factory (i.e. create_app):
    #         register_middlewares(app, settings["version"], settings["config"])
    #         Flask application can register more than one before_request/after_request.
    #         Beware! Before/after request callback stored internally in a dictionary.
    #         Before CPython 3.6 dictionaries didn't guarantee keys order, so callbacks
    #         could be executed in arbitrary order.
    #         """
    #         self._app.before_request(self.before_request)
    #         self._app.after_request(self.after_request)

    #     elif isinstance(self._app, FastAPI):
    #         self._app.mount("/metrics", WSGIMiddleware(make_wsgi_app()))

    #         @self._app.middleware("http")
    #         async def add_process_time_header(request: fastapi_request, call_next):

    #             self.before_request()

    #             response = await call_next(request)

    #             self.after_request(response, request)

    #             return response

    def before_request(self):
        """
        Get start time of a request
        """
        print("\n__START MIDDLEWARE : ..")
        self.request._prometheus_metrics_request_start_time = time.time()

    # def after_request(self, response):
    #     """
    #     Register Prometheus metrics after each request
    #     """

    #     request_latency = (
    #         time.time() - self.request._prometheus_metrics_request_start_time
    #     )
    #     if isinstance(self._app, Flask):
    #         self.METRICS_REQUEST_LATENCY_HISTOGRAM.labels(
    #             self.request.method, self.request.path, response.status_code
    #         ).observe(request_latency)
    #         self.METRICS_REQUEST_LATENCY_SUMMARY.labels(
    #             self.request.method, self.request.path, response.status_code
    #         ).observe(request_latency)
    #         self.METRICS_REQUEST_COUNT.labels(
    #             self.request.method, self.request.path, response.status_code
    #         ).inc()
    #         print("__END MIDDLEWARE : ..\n")

    #     elif isinstance(self._app, FastAPI):
    #         self.METRICS_REQUEST_LATENCY_HISTOGRAM.labels(
    #             self.request.method, self.request.url.path, response.status_code
    #         ).observe(request_latency)
    #         self.METRICS_REQUEST_LATENCY_SUMMARY.labels(
    #             self.request.method, self.request.url.path, response.status_code
    #         ).observe(request_latency)
    #         self.METRICS_REQUEST_COUNT.labels(
    #             self.request.method, self.request.url.path, response.status_code
    #         ).inc()
    #         print("__END MIDDLEWARE : ..\n")

    #     return response

    def add_flask_middleware(self):
        self._app.wsgi_app = DispatcherMiddleware(
            self._app.wsgi_app, {"/metrics": make_wsgi_app()}
        )
        """
        Register metrics middlewares
        Use in your application factory (i.e. create_app):
        register_middlewares(app, settings["version"], settings["config"])
        Flask application can register more than one before_request/after_request.
        Beware! Before/after request callback stored internally in a dictionary.
        Before CPython 3.6 dictionaries didn't guarantee keys order, so callbacks
        could be executed in arbitrary order.
        """

        def flask_after_request(response):

            request_latency = (
                time.time() - self.request._prometheus_metrics_request_start_time
            )
            self.METRICS_REQUEST_LATENCY_HISTOGRAM.labels(
                self.request.method, self.request.path, response.status_code
            ).observe(request_latency)
            self.METRICS_REQUEST_LATENCY_SUMMARY.labels(
                self.request.method, self.request.path, response.status_code
            ).observe(request_latency)
            self.METRICS_REQUEST_COUNT.labels(
                self.request.method, self.request.path, response.status_code
            ).inc()
            print("__END MIDDLEWARE : ..")
            return response

        self._app.before_request(self.before_request)
        self._app.after_request(flask_after_request)

    def add_fastapi_middleware(self):
        self._app.mount("/metrics", WSGIMiddleware(make_wsgi_app()))

        def fastapi_after_reqiest(response, request):
            request_latency = (
                time.time() - request._prometheus_metrics_request_start_time
            )
            self.METRICS_REQUEST_LATENCY_HISTOGRAM.labels(
                request.method, request.url.path, response.status_code
            ).observe(request_latency)
            self.METRICS_REQUEST_LATENCY_SUMMARY.labels(
                request.method, request.url.path, response.status_code
            ).observe(request_latency)
            self.METRICS_REQUEST_COUNT.labels(
                request.method, request.url.path, response.status_code
            ).inc()
            print("__END MIDDLEWARE : ..")
            return response

        @self._app.middleware("http")
        async def add_process_time_header(request: fastapi_request, call_next):

            self.before_request()
            response = await call_next(request)
            fastapi_after_reqiest(response, request)

            return response
