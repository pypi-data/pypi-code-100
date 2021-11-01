import time
import os
import re


import fastapi

from flask import Flask
from flask import request as flask_request
from fastapi import FastAPI
from fastapi import Request as fastapi_request
from fastapi.middleware.wsgi import WSGIMiddleware

from prometheus_client import Counter, Histogram, Summary, Info
from prometheus_client import make_wsgi_app
from prometheus_client import REGISTRY as PROMETHEUS_REGISTRY

# from prometheus_client
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from ..utils.singleton import SingletonMeta
from ..utils.bcolor import Bcolors
from .config import _DEFAULT_BUCKETS, _DEFAULT_LABELS, NAMESPACE, SERVICENAME


class PrometheusMiddleware(metaclass=SingletonMeta):

    # DONE: add serviceName and namespace(dev,beta,staging) to label (must have default value and can assign from env)
    # DONE: config default label
    # DONE: change bucket range for histogram and Summary
    # DONE: test for regEx route from request.path.___
    # TODO: percentile for summary
    # TODO: check async for fastapi
    # TODO: add readme.md and ..
    # TODO: add test for bracket
    # TODO: check read env
    # os.environ['SERVICE_NAME_PREFIX']
    # TODO: add warn seperately -> Please provide SERVICE_NAME_PREFIX and SERVICE_NAME in .env file

    namespace = NAMESPACE
    service_name = SERVICENAME

    _DEFAULT_BUCKETS = _DEFAULT_BUCKETS

    METRICS_REQUEST_LATENCY_HISTOGRAM = Histogram(
        "http_request_duration_ht_ms",
        "Duration of HTTP requests in ms (Histogram)",
        labelnames=_DEFAULT_LABELS,
        buckets=_DEFAULT_BUCKETS,
    )

    METRICS_REQUEST_LATENCY_SUMMARY = Summary(
        "http_request_duration_summary_ms",
        "Duration of HTTP requests in ms (Summary)",
        labelnames=_DEFAULT_LABELS,
    )

    METRICS_REQUEST_COUNT = Counter(
        "http_request_total",
        "Number of HTTP requests",
        labelnames=_DEFAULT_LABELS,
    )

    METRICS_INFO = Info("app_version", "Application Version")

    def __init__(
        self,
        app,
        namespace: str = None,
        serviceName: str = None,
        app_version: str = None,
    ):
        """
        :param app: web application framework can be either 'Flask' or 'fastapi' instance.
        :type app: 'astapi.applications.FastAPI' or 'flask.app.Flask'

        :param exclude_list: list of dict that contain atleast 1 key from this list ["method","route","status_code"]
        :type exclude_list: list of dict
        :example exclude_list = [{"route":"/index"}]  # this will exclude route : "/index" from being collect default metric
        :example exclude_list = [{"route":"/index","method":"get"}]  # this will exclude route : "/index" , method : "get" from being collect default metric

        """
        self.app = app
        self.exclude_list = [
            {"route": "/metrics/"},
            {"route": "/metrics"},
            {"route": "/metrics/{path}"},
        ]
        self._is_registered = False

        if app_version:
            self.METRICS_INFO.info({"version": app_version})

        if namespace:
            self.namespace = namespace
        if serviceName:
            self.service_name = serviceName
        self._check_env(self.namespace, self.service_name)

    @staticmethod
    def _check_invalid_exclude_format(list_input):
        """
        raise an error when invalid exclude format is found.
        """
        tuple_keys = ("method", "route", "status_code")
        for idx, val in reversed(list(enumerate(list_input))):
            if not isinstance(val, dict):
                error_msg = f"{Bcolors.FAIL}ERROR : Invalid exclude found : '{val}' is not valid exclude format. exclude must be instance of dict(){Bcolors.ENDC}"
                list_input.pop(idx)
                raise TypeError(error_msg)
            elif not any(key in val.keys() for key in tuple_keys):
                error_msg = f'{Bcolors.FAIL}ERROR : Invalid exclude found : \'{val}\' is not valid exclude format. exclude must contain atleast 1 key from this list ["method","route","status_code"]{Bcolors.ENDC}'
                list_input.pop(idx)
                raise ValueError(error_msg)
            elif "route" in val.keys():
                if val["route"][0] != "/":
                    warning_msg = f"{Bcolors.WARNING}WARNING : exclude {val} route's value is not start with '/'. This exclude will likely to be ignored{Bcolors.ENDC}"
                    print(warning_msg)
        return list_input

    def _check_env(self, namespace, serviceName):
        if (
            namespace == "UNDEFINED"
            or namespace is None
            or serviceName == "UNDEFINED"
            or serviceName is None
        ):
            print(
                f"{Bcolors.WARNING}WARNING: env variable : 'namespace' or 'serviceName' are not found.\nPlease provide SERVICE_NAME_PREFIX and SERVICE_NAME in .env file{Bcolors.ENDC}"
            )

    def clear_default_metrics(self):
        """
        Clear all observed default metrics.
        Generally being use in testing only.
        """
        for default_metric in self.default_metrics:
            default_metric.clear()

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
    def exclude_list(self, value: list):
        if isinstance(value, list):
            value = self._check_invalid_exclude_format(value)
            self._exclude_list = value
        else:
            raise TypeError("Invalid PrometheusMiddleware.exclude format")

    @property
    def default_metrics(self):
        """
        return a list of default metrics.
        """
        list_default_metrics = [
            self.METRICS_INFO,
            self.METRICS_REQUEST_LATENCY_HISTOGRAM,
            self.METRICS_REQUEST_LATENCY_SUMMARY,
            self.METRICS_REQUEST_COUNT,
        ]
        return list_default_metrics

    @property
    def default_exclude_list(self):
        return [{"route": "/metrics/"}, {"route": "/metrics"}]

    @property
    def PROMETHEUS_REGISTRY(self):
        """
        return REGISTRY object from prometheus client
        PROMETHEUS_REGISTRY can be use to access colleted metric
        Ex. PROMETHEUS_REGISTRY.get_sample_value(
            "http_request_duration_ht_ms_sum",
            labels={"http_status": "200", "method": "get", "route": "/sleep"},
            )
            this will retrieve data from "http_request_duration_ht_ms_sumq"
        """
        return PROMETHEUS_REGISTRY

    def add_exclude(self, added_exclude: list):
        """
        :param added_exclude: list of dict that contain atleast 1 key from this list ["method","route","status_code"]
        :type added_exclude: list(dict())
        Ex . [{"route":"/index"}] will exclude all metrics from route /index
        Ex . [{"route":"/index","status_code":"200"}] will exclude all metrics from route="/index" with status_code="200" (if error still collect metric)
        """
        list_buffer = self.exclude_list
        list_buffer.extend(added_exclude)
        self.exclude_list = list_buffer

    def is_exclude(self, method, route, status_code):
        """
        :param method: method of the endpoint
        :type method: str

        :param route: route of the endpoint
        :type route: str

        :param status_code: returned status of the request
        :type status_code: str
        """
        if not self.exclude_list:
            return False

        for exclude_item in self.exclude_list:
            cond_method = (
                True
                if exclude_item.get("method") is None
                else (exclude_item.get("method").lower() == method.lower())
            )
            cond_route = (
                True
                if exclude_item.get("route") is None
                else (exclude_item.get("route") == route)
            )
            cond_status_code = (
                True
                if exclude_item.get("status_code") is None
                else (exclude_item.get("status_code") == status_code)
            )

            if cond_method and cond_route and cond_status_code:
                return True

        return False

    def before_request(self):
        """
        Get start time of a request.
        This method get will call before a request processed.
        """
        self.request._prometheus_metrics_request_start_time = time.time()

    def add_flask_middleware(self):
        """
        Register metrics middlewares
        Flask application can register more than one before_request/after_request.
        Beware! Before/after request callback stored internally in a dictionary.
        Before CPython 3.6 dictionaries didn't guarantee keys order, so callbacks
        could be executed in arbitrary order.
        """

        self.app.wsgi_app = DispatcherMiddleware(
            self.app.wsgi_app, {"/metrics": make_wsgi_app()}
        )

        def flask_after_request(response):
            url_rule = (
                self.request.url_rule.rule
                if self.request.url_rule
                else self.request.path
            )
            if not self.is_exclude(self.request.method, url_rule, response.status_code):
                request_latency = (
                    time.time() - self.request._prometheus_metrics_request_start_time
                )
                self.METRICS_REQUEST_LATENCY_HISTOGRAM.labels(
                    self.request.method.lower(),
                    url_rule,
                    response.status_code,
                    self.service_name,
                    self.namespace,
                ).observe(request_latency)
                self.METRICS_REQUEST_LATENCY_SUMMARY.labels(
                    self.request.method.lower(),
                    url_rule,
                    response.status_code,
                    self.service_name,
                    self.namespace,
                ).observe(request_latency)
                self.METRICS_REQUEST_COUNT.labels(
                    self.request.method.lower(),
                    url_rule,
                    response.status_code,
                    self.service_name,
                    self.namespace,
                ).inc()
                print("observe..\n")
            return response

        self.app.before_request(self.before_request)
        self.app.after_request(flask_after_request)

    def add_fastapi_middleware(self):
        # TODO look into this later
        self.app.mount("/metrics", WSGIMiddleware(make_wsgi_app()))

        # NOTE: loop through all endpoint and get path_format
        def get_path_format(app_routes, path):
            path_format = path
            for route in app_routes:
                if re.search(route.path_regex, path) is not None:
                    return route.path_format
            return path_format

        def fastapi_after_request(response, request):
            path_format = get_path_format(request.app.routes, request.url.path)
            if not self.is_exclude(request.method, path_format, response.status_code):
                request_latency = (
                    time.time() - request._prometheus_metrics_request_start_time
                )
                self.METRICS_REQUEST_LATENCY_HISTOGRAM.labels(
                    request.method.lower(),
                    path_format,
                    response.status_code,
                    self.service_name,
                    self.namespace,
                ).observe(request_latency)
                self.METRICS_REQUEST_LATENCY_SUMMARY.labels(
                    request.method.lower(),
                    path_format,
                    response.status_code,
                    self.service_name,
                    self.namespace,
                ).observe(request_latency)
                self.METRICS_REQUEST_COUNT.labels(
                    request.method.lower(),
                    path_format,
                    response.status_code,
                    self.service_name,
                    self.namespace,
                ).inc()
                print("observe..\n")

            return response

        @self.app.middleware("http")
        async def add_process_time_header(request: fastapi_request, call_next):

            self.before_request()
            response = await call_next(request)
            fastapi_after_request(response, request)
            return response

    def register_metrics(self):
        """
        Register PrometheusMiddleware to collect all default metrics for all endpoint.
        With exception of condition is meet with excluded list.
        """
        if isinstance(self.app, Flask) and not self._is_registered:
            self.add_flask_middleware()
            self._is_registered = True
        elif isinstance(self.app, FastAPI) and not self._is_registered:
            self.add_fastapi_middleware()
            self._is_registered = True
