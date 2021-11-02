# Copyright (c) 2016-2018 Uber Technologies, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import logging
from abc import ABC, abstractmethod

from .constants import (
    _max_id_bits,
    SAMPLER_TYPE_CONST,
    SAMPLER_TYPE_PROBABILISTIC,
    SAMPLER_TYPE_RATE_LIMITING,
    SAMPLER_TYPE_LOWER_BOUND,
)
from .metrics import MetricsFactory
from .thrift import TagType
from .rate_limiter import RateLimiter
from typing import Any, Dict, Optional, Tuple


default_logger = logging.getLogger(__name__)


SAMPLER_TYPE_TAG_KEY = 'sampler.type'
SAMPLER_PARAM_TAG_KEY = 'sampler.param'
DEFAULT_SAMPLING_PROBABILITY = 0.001
DEFAULT_LOWER_BOUND = 1.0 / (10.0 * 60.0)  # sample once every 10 minutes
DEFAULT_MAX_OPERATIONS = 2000

STRATEGIES_STR = 'perOperationStrategies'
OPERATION_STR = 'operation'
DEFAULT_LOWER_BOUND_STR = 'defaultLowerBoundTracesPerSecond'
PROBABILISTIC_SAMPLING_STR = 'probabilisticSampling'
SAMPLING_RATE_STR = 'samplingRate'
DEFAULT_SAMPLING_PROBABILITY_STR = 'defaultSamplingProbability'
OPERATION_SAMPLING_STR = 'operationSampling'
MAX_TRACES_PER_SECOND_STR = 'maxTracesPerSecond'
RATE_LIMITING_SAMPLING_STR = 'rateLimitingSampling'
STRATEGY_TYPE_STR = 'strategyType'
PROBABILISTIC_SAMPLING_STRATEGY = 'PROBABILISTIC'
RATE_LIMITING_SAMPLING_STRATEGY = 'RATE_LIMITING'

TagsType = Dict[str, TagType]
IsSampledType = Tuple[bool, TagsType]


class BaseSampler(ABC):
    """
    Sampler is responsible for deciding if a particular span should be
    "sampled", i.e. recorded in permanent storage.
    """
    def __init__(self, tags: Optional[TagsType] = None):
        self._tags = tags or {}

    @abstractmethod
    def is_sampled(self, trace_id: int, operation: str = '') -> IsSampledType:
        pass

    async def close(self):
        pass

    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, self.__class__) and
            self.__dict__ == other.__dict__
        )

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)


class ConstSampler(BaseSampler):
    """ConstSampler always returns the same decision."""

    def __init__(self, decision: bool):
        super(ConstSampler, self).__init__(
            tags={
                SAMPLER_TYPE_TAG_KEY: SAMPLER_TYPE_CONST,
                SAMPLER_PARAM_TAG_KEY: decision,
            }
        )
        self.decision = decision

    def is_sampled(self, trace_id: int, operation: str = '') -> IsSampledType:
        return self.decision, self._tags

    def __str__(self) -> str:
        return 'ConstSampler(%s)' % self.decision


class ProbabilisticSampler(BaseSampler):
    """
    A sampler that randomly samples a certain percentage of traces specified
    by the samplingRate, in the range between 0.0 and 1.0.

    It relies on the fact that new trace IDs are 64bit random numbers
    themselves, thus making the sampling decision without generating a new
    random number, but simply calculating if traceID < (samplingRate * 2^64).
    Note that we actually ignore (zero out) the most significant bit.
    """

    def __init__(self, rate: float):
        super(ProbabilisticSampler, self).__init__(
            tags={
                SAMPLER_TYPE_TAG_KEY: SAMPLER_TYPE_PROBABILISTIC,
                SAMPLER_PARAM_TAG_KEY: rate,
            }
        )
        assert 0.0 <= rate <= 1.0, 'Sampling rate must be between 0.0 and 1.0'
        self.rate = rate
        self.max_number = 1 << _max_id_bits
        self.boundary = rate * self.max_number

    def is_sampled(self, trace_id: int, operation: str = '') -> IsSampledType:
        trace_id = trace_id & (self.max_number - 1)
        return trace_id < self.boundary, self._tags

    def __str__(self) -> str:
        return 'ProbabilisticSampler(%s)' % self.rate


class RateLimitingSampler(BaseSampler):
    """
    Samples at most max_traces_per_second. The distribution of sampled
    traces follows burstiness of the service, i.e. a service with uniformly
    distributed requests will have those requests sampled uniformly as well,
    but if requests are bursty, especially sub-second, then a number of
    sequential requests can be sampled each second.
    """

    def __init__(self, max_traces_per_second: float = 10):
        super(RateLimitingSampler, self).__init__()
        # value is set below
        self.rate_limiter: RateLimiter = None  # type:ignore
        self._init(max_traces_per_second)

    def _init(self, max_traces_per_second):
        assert max_traces_per_second >= 0, \
            'max_traces_per_second must not be negative'
        self._tags = {
            SAMPLER_TYPE_TAG_KEY: SAMPLER_TYPE_RATE_LIMITING,
            SAMPLER_PARAM_TAG_KEY: max_traces_per_second,
        }
        self.traces_per_second = max_traces_per_second
        max_balance = max(self.traces_per_second, 1.0)
        if not self.rate_limiter:
            self.rate_limiter = RateLimiter(
                credits_per_second=self.traces_per_second,
                max_balance=max_balance
            )
        else:
            self.rate_limiter.update(max_traces_per_second, max_balance)

    def is_sampled(self, trace_id: int, operation: str = '') -> IsSampledType:
        return self.rate_limiter.check_credit(1.0), self._tags

    def __eq__(self, other: Any) -> bool:
        """The last_tick and balance fields can be different"""
        if not isinstance(other, self.__class__):
            return False
        d1 = dict(self.rate_limiter.__dict__)
        d2 = dict(other.rate_limiter.__dict__)
        d1['balance'] = d2['balance']
        d1['last_tick'] = d2['last_tick']
        return d1 == d2

    def update(self, max_traces_per_second: float) -> bool:
        if self.traces_per_second == max_traces_per_second:
            return False
        self._init(max_traces_per_second)
        return True

    def __str__(self) -> str:
        return 'RateLimitingSampler(%s)' % self.traces_per_second


class GuaranteedThroughputProbabilisticSampler(BaseSampler):
    """
    A sampler that leverages both ProbabilisticSampler and RateLimitingSampler.
    The RateLimitingSampler is used as a guaranteed lower bound sampler such
    that every operation is sampled at least once in a time interval defined by
    the lower_bound. ie a lower_bound of 1.0 / (60 * 10) will sample an
    operation at least once every 10 minutes.

    The ProbabilisticSampler is given higher priority when tags are emitted,
    ie. if is_sampled() for both samplers return true, the tags for
    ProbabilisticSampler will be used.
    """
    def __init__(self, operation: str, lower_bound: float, rate: float):
        super(GuaranteedThroughputProbabilisticSampler, self).__init__(
            tags={
                SAMPLER_TYPE_TAG_KEY: SAMPLER_TYPE_LOWER_BOUND,
                SAMPLER_PARAM_TAG_KEY: rate,
            }
        )
        self.probabilistic_sampler = ProbabilisticSampler(rate)
        self.lower_bound_sampler = RateLimitingSampler(lower_bound)
        self.operation = operation
        self.rate = rate
        self.lower_bound = lower_bound

    def is_sampled(self, trace_id: int, operation: str = '') -> IsSampledType:
        sampled, tags = \
            self.probabilistic_sampler.is_sampled(trace_id, operation)
        if sampled:
            self.lower_bound_sampler.is_sampled(trace_id, operation)
            return True, tags
        sampled, _ = self.lower_bound_sampler.is_sampled(trace_id, operation)
        return sampled, self._tags

    async def close(self):
        await self.probabilistic_sampler.close()
        await self.lower_bound_sampler.close()

    def update(self, lower_bound: int, rate: float):
        # (NB) This function should only be called while holding a Write lock.
        if self.rate != rate:
            self.probabilistic_sampler = ProbabilisticSampler(rate)
            self.rate = rate
            self._tags = {
                SAMPLER_TYPE_TAG_KEY: SAMPLER_TYPE_LOWER_BOUND,
                SAMPLER_PARAM_TAG_KEY: rate,
            }
        if self.lower_bound != lower_bound:
            self.lower_bound_sampler.update(lower_bound)
            self.lower_bound = lower_bound

    def __str__(self) -> str:
        return 'GuaranteedThroughputProbabilisticSampler(%s, %f, %f)' \
               % (self.operation, self.rate, self.lower_bound)


class AdaptiveSampler(BaseSampler):
    """
    A sampler that leverages both ProbabilisticSampler and RateLimitingSampler
    via the GuaranteedThroughputProbabilisticSampler. This sampler keeps track
    of all operations and delegates calls the the respective
    GuaranteedThroughputProbabilisticSampler.
    """
    def __init__(self, strategies: Dict[str, Any], max_operations: int):
        super(AdaptiveSampler, self).__init__()

        samplers = {}
        for strategy in strategies.get(STRATEGIES_STR, []):
            operation = strategy.get(OPERATION_STR)
            sampler = GuaranteedThroughputProbabilisticSampler(
                operation,
                strategies.get(DEFAULT_LOWER_BOUND_STR, DEFAULT_LOWER_BOUND),
                get_sampling_probability(strategy)
            )
            samplers[operation] = sampler

        self.samplers = samplers
        self.default_sampler = ProbabilisticSampler(
                strategies.get(
                    DEFAULT_SAMPLING_PROBABILITY_STR,
                    DEFAULT_SAMPLING_PROBABILITY
                )
        )
        self.default_sampling_probability = strategies.get(
            DEFAULT_SAMPLING_PROBABILITY_STR, DEFAULT_SAMPLING_PROBABILITY
        )
        self.lower_bound = strategies.get(
            DEFAULT_LOWER_BOUND_STR, DEFAULT_LOWER_BOUND
        )
        self.max_operations = max_operations

    def is_sampled(self, trace_id: int, operation: str = '') -> IsSampledType:
        sampler = self.samplers.get(operation)
        if not sampler:
            if len(self.samplers) >= self.max_operations:
                return self.default_sampler.is_sampled(trace_id, operation)
            sampler = GuaranteedThroughputProbabilisticSampler(
                operation,
                self.lower_bound,
                self.default_sampling_probability
            )
            self.samplers[operation] = sampler
            return sampler.is_sampled(trace_id, operation)
        return sampler.is_sampled(trace_id, operation)

    def update(self, strategies: Dict[str, Any]):
        # (NB) This function should only be called while holding a Write lock.
        for strategy in strategies.get(STRATEGIES_STR, []):
            operation = strategy.get(OPERATION_STR)
            lower_bound = strategies.get(
                DEFAULT_LOWER_BOUND_STR, DEFAULT_LOWER_BOUND
            )
            sampling_rate = get_sampling_probability(strategy)
            sampler = self.samplers.get(operation)
            if not sampler:
                sampler = GuaranteedThroughputProbabilisticSampler(
                    operation,
                    lower_bound,
                    sampling_rate
                )
                self.samplers[operation] = sampler
            else:
                sampler.update(lower_bound, sampling_rate)
        self.lower_bound = strategies.get(
            DEFAULT_LOWER_BOUND_STR, DEFAULT_LOWER_BOUND
        )
        if self.default_sampling_probability != strategies.get(
                DEFAULT_SAMPLING_PROBABILITY_STR, DEFAULT_SAMPLING_PROBABILITY
        ):
            self.default_sampling_probability = strategies.get(
                DEFAULT_SAMPLING_PROBABILITY_STR, DEFAULT_SAMPLING_PROBABILITY
            )
            self.default_sampler = ProbabilisticSampler(
                self.default_sampling_probability
            )

    async def close(self):
        for _, sampler in self.samplers.items():
            await sampler.close()

    def __str__(self) -> str:
        return 'AdaptiveSampler(%f, %f, %d)' \
               % (self.default_sampling_probability, self.lower_bound,
                  self.max_operations)


def get_sampling_probability(
        strategy: Optional[Dict[str, Any]] = None
) -> float:
    if not strategy:
        return DEFAULT_SAMPLING_PROBABILITY
    probability_strategy = strategy.get(PROBABILISTIC_SAMPLING_STR)
    if not probability_strategy:
        return DEFAULT_SAMPLING_PROBABILITY
    return probability_strategy.get(
        SAMPLING_RATE_STR, DEFAULT_SAMPLING_PROBABILITY
    )


def get_rate_limit(strategy: Optional[Dict[str, Any]] = None) -> float:
    if not strategy:
        return DEFAULT_LOWER_BOUND
    rate_limit_strategy = strategy.get(RATE_LIMITING_SAMPLING_STR)
    if not rate_limit_strategy:
        return DEFAULT_LOWER_BOUND
    return rate_limit_strategy.get(
        MAX_TRACES_PER_SECOND_STR, DEFAULT_LOWER_BOUND
    )


class SamplerMetrics(object):
    """Sampler specific metrics."""

    def __init__(self, metrics_factory: MetricsFactory):
        self.sampler_retrieved = metrics_factory.create_counter(
            name='jaeger:sampler_queries', tags={'result': 'ok'}
        )
        self.sampler_query_failure = metrics_factory.create_counter(
            name='jaeger:sampler_queries', tags={'result': 'err'}
        )
        self.sampler_updated = metrics_factory.create_counter(
            name='jaeger:sampler_updates', tags={'result': 'ok'}
        )
        self.sampler_update_failure = metrics_factory.create_counter(
            name='jaeger:sampler_updates', tags={'result': 'err'}
        )
