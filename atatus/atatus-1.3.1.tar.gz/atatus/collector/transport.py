
import json
import requests
from .builder import Builder
from atatus.utils import compat
from atatus.utils.logging import get_logger
import atatus
import time

class BaseTransport(object):
    def __init__(self, config, metadata):
        self._config = config
        self._error_logger = get_logger("atatus.errors")
        self._notify_host = config.notify_host if config.notify_host.endswith("/") else config.notify_host + "/"
        self._builder = Builder(config, metadata)
        # self._session = requests.Session()
        self._blocked = False
        self._capture_percentiles = False
        self._post_params = {
            'license_key': self._config.license_key,
            'agent_name': atatus.PYTHON_AGENT,
            "version": atatus.VERSION
        }

    def _post(self, endpoint, data):
        if (self._blocked is True) and (endpoint != 'track/apm/hostinfo'):
            return

        try:
            time.sleep(0.01)
            r = requests.post(self._notify_host + endpoint, params=self._post_params, timeout=30, json=data)

            self._blocked = False

            if r.status_code == 200:
                if endpoint == 'track/apm/hostinfo':
                    self._capture_percentiles = False
                    c = r.content
                    if not c:
                        return

                    if compat.PY3:
                        c = c.decode('UTF-8')

                    resp = json.loads(c)
                    if resp:
                        if "capturePercentiles" in resp:
                            self._capture_percentiles = resp["capturePercentiles"]

                return

            if r.status_code == 400:
                c = r.content
                if not c:
                    self._error_logger.error("Atatus transport status 400, failed without content")
                    return

                if compat.PY3:
                    c = c.decode('UTF-8')

                resp = json.loads(c)
                if resp:
                    if "blocked" in resp:
                        self._blocked = resp["blocked"]
                        if self._blocked is True:
                            if "errorMessage" in resp:
                                self._error_logger.error(
                                    "Atatus blocked from sending data as: %s ", resp["errorMessage"])
                                return

                self._error_logger.error("Atatus transport status 400, failed with content: %r", c)
                return

            if r.status_code != 200:
                self._error_logger.error(
                    "Atatus transport unexpected non-200 response [%s] [status_code: %r]." % (self._notify_host + endpoint, r.status_code))

        except Exception as e:
            self._error_logger.error(
                "Atatus transport [%r] failed with exception: %r", self._notify_host + endpoint, e)
            raise

    def hostinfo(self, start_time):
        payload = self._builder.hostinfo(start_time)
        self._post('track/apm/hostinfo', payload)

    def txns(self, start_time, end_time, data):
        payload = self._builder.txns(start_time, end_time, data)
        self._post('track/apm/txn', payload)

    def txn_hist(self, start_time, end_time, data):
        if self._capture_percentiles is True:
            payload = self._builder.txn_hist(start_time, end_time, data)
            self._post('track/apm/txn/histogram', payload)

    def traces(self, start_time, end_time, data):
        payload = self._builder.traces(start_time, end_time, data)
        self._post('track/apm/trace', payload)

    def error_metrics(self, start_time, end_time, metrics_data, requests_data):
        payload = self._builder.error_metrics(start_time, end_time, metrics_data, requests_data)
        self._post('track/apm/error_metric', payload)

    def errors(self, start_time, end_time, error_data):
        payload = self._builder.errors(start_time, end_time, error_data)
        self._post('track/apm/error', payload)

    def metrics(self, start_time, end_time, metrics_data):
        payload = self._builder.metrics(start_time, end_time, metrics_data)
        self._post('track/apm/metric', payload)
