from typing import Any, Callable

from jetpack._job.job import Job as _Job
from jetpack.config import symbols


class JobDecorator:
    def __call__(self, fn: Callable[..., Any]) -> Callable[..., Any]:
        job = _Job(fn)
        symbols.get_symbol_table().register(fn)
        return job


job = JobDecorator()
