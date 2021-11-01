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

from ..utils.singleton import SingletonMeta


class PrometheusMiddleware(metaclass=SingletonMeta):
    def __init__(self, app):
        """
        :param app: web application framework can be either 'Flask' or 'fastapi' instance.
        :type app: 'astapi.applications.FastAPI' or 'flask.app.Flask'

        :param exclude_list: list of dict that contain atleast 1 key from this list ["method","route","status_code"]
        :type exclude_list: list of dict
        :example exclude_list = [{"route":"/index"}]  # this will exclude route : "/index" from being collect default metric
        :example exclude_list = [{"route":"/index","method":"get"}]  # this will exclude route : "/index" , method : "get" from being collect default metric

        """
        self.app = app
        self.exclude_list = list()
        self.exclude_route = dict()

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

    @staticmethod
    def remove_invalid_exclude_format(list_input):
        tuple_keys = ("method", "route", "status_code")
        for idx, val in reversed(list(enumerate(list_input))):
            if not isinstance(val, dict):
                print(
                    f"WARNING : Invalid exclude found : '{val}' is not valid exclude format. This exclude will be ignore"
                )
                list_input.pop(idx)
            elif not any(key in val.keys() for key in tuple_keys):
                print(
                    f"WARNING : Invalid exclude found : '{val}' is not valid exclude format. This exclude will be ignore"
                )
                list_input.pop(idx)
        return list_input

    @property
    def app(self):
        return self._app

    @app.setter
    def app(self, new_app):
        if isinstance(new_app, Flask):
            self._app = new_app
            self.request = flask_request
        elif isinstance(new_app, FastAPI):
            self._app = new_app
            self.request = fastapi_request
        else:
            raise TypeError("app type have to be etiher 'Flask' or 'fastapi'.")

    @property
    def request(self):
        return self._request

    @request.setter
    def request(self, request_class):
        self._request = request_class

    @property
    def exclude_list(self):
        return self._exclude_list

    @exclude_list.setter
    def exclude_list(self, value):
        _DEFAULT_EXCLUDE_METRICS_ROUTE = [{"route": "/metrics/"}, {"route": "/metrics"}]
        if isinstance(value, list):
            value.extend(_DEFAULT_EXCLUDE_METRICS_ROUTE)
            value = self.remove_invalid_exclude_format(value)
            self._exclude_list = value
        else:
            raise TypeError("Invalid PrometheusMiddleware.exclude format")

    @property
    def default_metrics(self):
        list_default_metrics = [
            self.METRICS_INFO,
            self.METRICS_REQUEST_LATENCY_HISTOGRAM,
            self.METRICS_REQUEST_LATENCY_SUMMARY,
            self.METRICS_REQUEST_COUNT,
        ]
        return list_default_metrics

    def is_exclude(self, method, route, status_code):

        if not self.exclude_list:
            return False

        for exclude_item in self.exclude_list:
            cond_method = (
                True
                if not exclude_item.get("method")
                else (exclude_item.get("method") == method)
            )
            cond_route = (
                True
                if not exclude_item.get("route")
                else (exclude_item.get("route") == route)
            )
            cond_status_code = (
                True
                if not exclude_item.get("status_code")
                else (exclude_item.get("status_code") == status_code)
            )

            if cond_method and cond_route and cond_status_code:
                return True

        return False

    def before_request(self):
        """
        Get start time of a request
        """
        self.request._prometheus_metrics_request_start_time = time.time()

    def add_flask_middleware(self):
        """
        Register metrics middlewares
        Use in your application factory (i.e. create_app):
        register_middlewares(app, settings["version"], settings["config"])
        Flask application can register more than one before_request/after_request.
        Beware! Before/after request callback stored internally in a dictionary.
        Before CPython 3.6 dictionaries didn't guarantee keys order, so callbacks
        could be executed in arbitrary order.
        """

        self.app.wsgi_app = DispatcherMiddleware(
            self.app.wsgi_app, {"/metrics": make_wsgi_app()}
        )

        def flask_after_request(response):
            if not self.is_exclude(
                self.request.method, self.request.path, response.status_code
            ):
                request_latency = (
                    time.time() - self.request._prometheus_metrics_request_start_time
                )
                self.METRICS_REQUEST_LATENCY_HISTOGRAM.labels(
                    self.request.method.lower(), self.request.path, response.status_code
                ).observe(request_latency)
                self.METRICS_REQUEST_LATENCY_SUMMARY.labels(
                    self.request.method.lower(), self.request.path, response.status_code
                ).observe(request_latency)
                self.METRICS_REQUEST_COUNT.labels(
                    self.request.method.lower(), self.request.path, response.status_code
                ).inc()
                print("observe..")
                return response

        print("\n__BEFORE REQUEST : ..")
        self.app.before_request(self.before_request)
        self.app.after_request(flask_after_request)
        print("__AFTER REQUEST : ..")

    def add_fastapi_middleware(self):
        self.app.mount("/metrics", WSGIMiddleware(make_wsgi_app()))

        def fastapi_after_reqiest(response, request):
            if not self.is_exclude(
                request.method, request.url.path, response.status_code
            ):
                request_latency = (
                    time.time() - request._prometheus_metrics_request_start_time
                )
                self.METRICS_REQUEST_LATENCY_HISTOGRAM.labels(
                    request.method.lower(), request.url.path, response.status_code
                ).observe(request_latency)
                self.METRICS_REQUEST_LATENCY_SUMMARY.labels(
                    request.method.lower(), request.url.path, response.status_code
                ).observe(request_latency)
                self.METRICS_REQUEST_COUNT.labels(
                    request.method.lower(), request.url.path, response.status_code
                ).inc()
                print("observe..")

                return response

        @self.app.middleware("http")
        async def add_process_time_header(request: fastapi_request, call_next):

            print("\n__BEFORE REQUEST : ..")
            self.before_request()
            response = await call_next(request)
            fastapi_after_reqiest(response, request)
            print("__AFTER REQUEST : ..")
            return response

    def register_metrics(self, app_version=None, app_config=None):
        if isinstance(self.app, Flask):
            self.add_flask_middleware()
        elif isinstance(self.app, FastAPI):
            self.add_fastapi_middleware()
