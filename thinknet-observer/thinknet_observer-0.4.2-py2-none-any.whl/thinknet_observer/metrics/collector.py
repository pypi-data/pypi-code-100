import prometheus_client

# from prometheus_client import Counter,Summary,Histogram,Gauge

from .config import _DEFAULT_BUCKETS
from .config import NAMESPACE, SERVICENAME, DICT_REQURIED_LABELS
from .custom_metrics_wrapper import (
    CounterWrapper,
    SummaryWrapper,
    HistogramWrapper,
    GaugeWrapper,
)
from ..utils.bcolor import Bcolors


class MetricCollector:
    def __init__(self) -> None:
        pass

    @staticmethod
    def _add_default_label(input_labels: list):
        for expected_label in DICT_REQURIED_LABELS:
            if expected_label not in input_labels:
                input_labels.append(expected_label)
        return input_labels

    @classmethod
    def gauge(
        cls,
        name: str,
        documentation: str,
        labels: list = [],
    ):
        """
        Gauge usage is like counter but can be decrease(.dec()) as well as increase(.inc())

        :param name: name of the gauge.
        :type name: str

        :param documentation: description of this metric.
        :type documentation: str

        :param labels: (Optional)labels of this gauge.
        :type labels: tuple

        :return: gauge object
        :rtype: prometheus_client.Counter Object
        """
        labels = cls._add_default_label(labels)
        metric_guage = prometheus_client.Gauge(name, documentation, labelnames=labels)
        warpped_guage = GaugeWrapper(metric_guage)
        return warpped_guage

    @classmethod
    def histogram(
        cls,
        name: str,
        documentation: str,
        labels: list = [],
        buckets=_DEFAULT_BUCKETS,
    ):
        """
        :param name: name of the histogram.
        :type name: str

        :param documentation: description of this metric.
        :type documentation: str

        :param labels: (Optional)labels of this histogram.
        :type labels: tuple

        :param buckets: (Optional)buckets of this histogram Ex buckets=(1,2,3,5,10).
        :type buckets: list

        :return: histogram object
        :rtype: prometheus_client.Counter Object
        """
        labels = cls._add_default_label(labels)
        metric_histogram = prometheus_client.Histogram(
            name,
            documentation,
            labelnames=labels,
            buckets=buckets,
        )
        warpped_histogram = HistogramWrapper(metric_histogram)
        return warpped_histogram

    @classmethod
    def summary(cls, name: str, documentation: str, labels: list = []):
        """
        A Summary tracks the size and number of events.

        :param name: name of the summary.
        :type name: str

        :param documentation: description of this metric.
        :type documentation: str

        :param labels: (Optional)labels of this summary.
        :type labels: tuple

        :return: summary object
        :rtype: prometheus_client.Counter Object

        Example use cases for Summary:

        Response latency
        Request size
        """
        labels = cls._add_default_label(labels)
        metric_summary = prometheus_client.Summary(
            name, documentation, labelnames=labels
        )
        warpped_summary = SummaryWrapper(metric_summary)

        return warpped_summary

    @classmethod
    def counter(cls, name: str, documentation: str, labels: list = []):
        """
        create counter metrics

        :param name: name of the counter.
        :type name: str

        :param documentation: description of this metric.
        :type documentation: str

        :param labels: (Optional)labels of this counter.
        :type labels: tuple

        :return: counter object
        :rtype: prometheus_client.Counter Object

        Example

        c = counter('my_failures_total', 'Description of counter')
        c.inc() # Increment by 1
        c.inc(1.6) # Increment by given value

        There are utilities to count exceptions raised:
        @c.count_exceptions() def f():
            pass

        with c.count_exceptions():
            pass

        # Count only one type of exception with c.count_exceptions(ValueError):
            pass
        """

        labels_added = cls._add_default_label(labels)
        metric_counter = prometheus_client.Counter(
            name,
            documentation,
            labelnames=labels_added,
        )
        warpped_counter = CounterWrapper(metric_counter)

        return warpped_counter
