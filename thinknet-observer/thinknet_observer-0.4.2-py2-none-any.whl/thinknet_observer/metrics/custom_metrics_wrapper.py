from .config import _DEFAULT_BUCKETS
from .config import NAMESPACE, SERVICENAME, DICT_REQURIED_LABELS


def add_default_label_value(func):
    """Decorator that add default label to the custom metrics"""

    def wrap(*args, **kwargs):
        if kwargs:
            for key in DICT_REQURIED_LABELS:
                if not kwargs.get(key):
                    kwargs.update({key: DICT_REQURIED_LABELS[key]})
        elif args:
            list_args = list(args)
            for requried_label in DICT_REQURIED_LABELS.keys():
                if requried_label not in list_args:
                    list_args.append(DICT_REQURIED_LABELS[requried_label])
            args = tuple(list_args)

        result = func(*args, **kwargs)

        return result

    return wrap


class CustomMetricsWrapperBase(object):
    """
    This Class use to warp Metrics class so that it will be include default label's value autometiclly when observed/used
    """

    def __init__(self, obj):
        self._wrapped_obj = obj

    @add_default_label_value
    def labels(self, *args, **kwargs):
        if kwargs:
            return self._wrapped_obj.labels(**kwargs)
        elif args:
            return self._wrapped_obj.labels(*args)

    def clear(self):
        self._wrapped_obj.clear()


class CounterWrapper(CustomMetricsWrapperBase):
    def __init__(self, obj):
        super().__init__(obj)

    def inc(self, *args):
        """Increment counter by the given amount."""
        super().labels().inc(*args)


class SummaryWrapper(CustomMetricsWrapperBase):
    def __init__(self, obj):
        super().__init__(obj)

    def observe(self, *args):
        """Observe the given amount.

        The amount is usually positive or zero. Negative values are
        accepted but prevent current versions of Prometheus from
        properly detecting counter resets in the sum of
        observations. See
        https://prometheus.io/docs/practices/histograms/#count-and-sum-of-observations
        for details.
        """
        super().labels().observe(*args)

    def time(self):
        """Time a block of code or function, and observe the duration in seconds.

        Can be used as a function decorator or context manager.
        """
        return super().labels().time()


class HistogramWrapper(CustomMetricsWrapperBase):
    def __init__(self, obj):
        super().__init__(obj)

    def observe(self, *args):
        """Observe the given amount.

        The amount is usually positive or zero. Negative values are
        accepted but prevent current versions of Prometheus from
        properly detecting counter resets in the sum of
        observations. See
        https://prometheus.io/docs/practices/histograms/#count-and-sum-of-observations
        for details.
        """
        super().labels().observe(*args)

    def time(self):
        """Time a block of code or function, and observe the duration in seconds.

        Can be used as a function decorator or context manager.
        """
        return super().labels().time()


class GaugeWrapper(CustomMetricsWrapperBase):
    def __init__(self, obj):
        super().__init__(obj)

    def inc(self, *args):
        """Increment gauge by the given amount."""
        super().labels().inc(*args)

    def dec(self, *args):
        """Decrement gauge by the given amount."""
        super().labels().dec(*args)

    def set(self, *args):
        """Set gauge to the current unixtime."""
        super().labels().set(*args)

    def track_inprogress():
        """Track inprogress blocks of code or functions.

        Can be used as a function decorator or context manager.
        Increments the gauge when the code is entered,
        and decrements when it is exited.
        """
        super().labels().track_inprogress()
