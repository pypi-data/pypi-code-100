from __future__ import annotations

import contextlib
import collections
import datetime
import argparse
import time
import types
import math
import pydoc
import collections
import functools
import itertools
import logging

import votakvot
import votakvot.core
import votakvot.meta

from votakvot.data import FancyDict


logger = logging.getLogger(__file__)


def _resolve_name(import_name):
    return pydoc.locate(import_name)


def _calc_percentiles(data, pcts):
    data = sorted(data)
    size = len(data)
    return {
        pct: data[int(math.ceil((size * pct) / 100)) - 1]
        for pct in pcts
    }


def _round_time(t):
    return round(t, 5)


def _ensure_either_notnone(a, b):
    if a is not None and b is not None:
        raise ValueError("Multiple non-None results from generator")
    return a if a is not None else b


class StatsCollector:

    def __init__(
        self,
        tracker: votakvot.core.Tracker,
        warmup: int = 0,
        progressbar: tqdm.tqdm | None = None,
        lock = None,
    ):
        self._lock = lock or contextlib.nullcontext()
        self._warmup = warmup
        self._started = time.time()
        self._finished = None
        self.tracker = tracker
        self.results = collections.Counter()
        self.total_count = 0
        self.total_time = 0
        self.errors = []
        self.times = []
        self.progressbar = progressbar

    def add_result(self, result, duration, error=None):
        with self._lock:
            self._add_result0(result, duration, error)

    def _add_result0(self, result, duration, error):

        if self._warmup > 0:
            self._warmup -= 1
            return
        elif self._warmup == 0:
            self._started = time.time()
            self._warmup = -1

        self.total_count += 1
        self.results[result] += 1
        self.tracker.meter({
            'duration': duration,
            'result': result,
            'error': repr(error) if error else None,
        })
        if duration is not None:
            self.times.append(duration)
            self.total_time += duration

        if error is not None:
            self.errors.append(error)

        if self.progressbar is not None:
            self.progressbar.update()

    def calculate_statistics(self):
        self._finished = self._finished or time.time()
        average = sum(self.times) / len(self.times) if self.times else None
        return FancyDict(
            total_count=self.total_count,
            total_time=self.total_time,
            real_rps=self.total_count / (self._finished - self._started),
            duration=FancyDict(
                average=_round_time(average),
                maximum=_round_time(max(self.times)),
                minimum=_round_time(min(self.times)),
                std_dev=round(math.sqrt(sum((x - average) ** 2 for x in self.times) / len(self.times)), 3),
                percentiles=_calc_percentiles(self.times, [25, 50, 75, 90, 95, 97, 98, 99]),
            ) if self.times else None,
            results=[
                {"result": k, "count": v}
                for k, v in self.results.most_common()
            ],
            errors_count=len(self.errors),
            errors=self.errors,
        )


def _do_onecall(collector: StatsCollector, callback, params):

    params = params or {}
    start = time.time()
    duration = None
    error = None
    res = None
    maybe_gen = None

    try:
        maybe_gen = callback(**params)
        if isinstance(maybe_gen, types.GeneratorType):
            res = next(maybe_gen)  # prepare
            start = time.time()    # reset time
            try:
                res = _ensure_either_notnone(next(maybe_gen), res)
            except StopIteration as si:
                res = _ensure_either_notnone(si.value, res)
                maybe_gen = None
        else:
            res = maybe_gen
            maybe_gen = None

    except Exception as e:
        error = e

    else:
        duration = time.time() - start

    finally:
        if maybe_gen:
            x = object()
            if next(maybe_gen, x) is not x:
                raise ValueError("Test callback must contain no more than one yield")
        collector.add_result(res, duration, error)


def _gevent_monkey_patch():
    import gevent.monkey
    gevent.monkey.patch_all()


class _GeventEnv:

    def __init__(self, concurrency):
        import gevent
        import gevent.pool
        self.semaphore = gevent.lock.Semaphore
        self.pool = gevent.pool.Pool(concurrency)
        self._timeout = gevent.Timeout

    def join(self):
        self.pool.join()

    def spawn(self, function):
        self.pool.spawn(function)

    def abort_after(self, duration):
        return self._timeout(duration, False)


def runit(
    path,
    callback,
    tid=None,
    params=None,
    number=1,
    warmup=0,
    duration=None,
    concurrency=1,
    meta_providers=None,
    show_progress=False,
    environment=None,
):
    import tqdm

    environment = environment or _GeventEnv(concurrency)
    meta = votakvot.meta.capture_meta(meta_providers)
    tracker = votakvot.core.Tracker(path=f"{path}/{tid}", meta=meta, tid=tid)
    progressbar = tqdm.tqdm(total=number, leave=False) if show_progress else None

    def dorun(**params):
        res = StatsCollector(tracker, warmup=warmup, progressbar=progressbar, lock=environment.semaphore())
        call = functools.partial(_do_onecall, res, callback, params)
        if number is None:
            with environment.abort_after(duration):
                while True:
                    environment.spawn(call)
        else:
            for _ in range(number + warmup):
                environment.spawn(call)

        environment.join()
        return res.calculate_statistics()

    with progressbar if progressbar is not None else contextlib.nullcontext():
        with votakvot.using_tracker(tracker):
            tracker.run(dorun, **(params or {}))
            return votakvot.core.Trial(tracker.path)


def main(args=None):

    _gevent_monkey_patch()

    parser = argparse.ArgumentParser(description="votakvot cli runner")
    parser.add_argument("-c", "--concurrency", help="Concurrency", type=int, default=1)
    parser.add_argument("-q", "--quiet", help="Don't display progress bar", action="store_true")
    parser.add_argument("-w", "--warmup", help="Number of skipped requests", default=0, type=int)
    parser.add_argument("-p", "--path", help="Path to results storage", type=str, default=".")
    parser.add_argument("-t", "--tid", help="Tid identifier", default=None)

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-n", "--number", help="Number of requests", type=int)
    group.add_argument("-d", "--duration", help="Duration in seconds", type=int)

    parser.add_argument("callback", type=_resolve_name, help="Python callable name")
    parser.add_argument("param", metavar="KEY=VALUE", nargs="*", help="Function named argument")

    opts = parser.parse_args(args)

    if opts.number is None and opts.duration is None:
        opts.number = 1

    callback_name = f"{opts.callback.__module__}.{opts.callback.__qualname__}"
    if opts.tid is None:
        dt_suffix = datetime.datetime.now().strftime("%y-%m-%d/%H:%M:%S")
        opts.tid = f"{callback_name}/{dt_suffix}"

    params = {}
    for p in opts.param:
        k, v = p.split("=", 1)
        if k in params:
            raise ValueError("Duplicated parameter", k)
        v = eval(v)
        params[k] = v

    if True:
        print(f"run '{callback_name}(" + ", ".join(f"{k}={v!r}" for k, v in params.items()) + ")'")
        print(f"use {opts.concurrency} parallel workers")

    if opts.number:
        print(f"make {opts.number} runs")
    else:
        print(f"keep running for {round(opts.duration)} seconds")

    if opts.warmup:
        print(f"skip {opts.warmup} first runs")

    print("running...")
    start_at = time.time()
    trial = runit(
        callback=opts.callback,
        params=params,
        path=opts.path,
        tid=opts.tid,
        number=opts.number,
        concurrency=opts.concurrency,
        duration=opts.duration,
        warmup=opts.warmup,
        show_progress=not opts.quiet,
    )
    res = trial.result

    print("done")
    print("")

    def ms(t):
        return "{:.2f} ms".format(1000 * t)

    if res.real_rps > 1000:
        print(f"warning: too high rps\nresults might be very unaccurate")
        print()

    print(f"was made  \t {res.total_count} runs")
    if res.duration:
        print(f"average \t {ms(res.duration.average)}")
        print(f"std_dev \t {ms(res.duration.std_dev)}")
        print(f"minimum \t {ms(res.duration.minimum)}")
        print(f"maximum \t {ms(res.duration.minimum)}")
        print(f"percentiles:")
        for pn, pv in res.duration.percentiles.items():
            print(f"  pct {pn:02}   \t {ms(pv)}")

    print(f"results:")
    for d in res.results:
        print(f"  {d.count} times \t {d.result!r}")

    if res.errors:
        print(f"occured {res.errors_count} errors:")
        show_n_errors = 10
        errors_list = list(res.errors)
        errors_list.sort(key=repr)
        errors_grouped = [list(g) for _, g in itertools.groupby(errors_list, key=repr)]
        errors_grouped.sort(key=len, reverse=True)
        for es in errors_grouped[:show_n_errors]:
            print(f"  {len(es)} times \t {es[0]!r}")
        if len(errors_grouped) > show_n_errors:
            print(f"  ... {res.errors_count - len(errors_grouped)} more ... ")
    else:
        print(f"no errors")
    print(f"more results at\n  {trial.path}")


if __name__ == "__main__":
    main()
