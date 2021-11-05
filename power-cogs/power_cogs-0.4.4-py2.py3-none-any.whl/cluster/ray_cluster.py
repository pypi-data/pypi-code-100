import typing

import attr
import ray
from ray.util import ActorPool

from power_cogs.cluster.cluster import Cluster
from power_cogs.cluster.execution import Execution
from power_cogs.config.cluster_config import RayClusterConfig
from power_cogs.config.config import class_config


@class_config(RayClusterConfig)
@attr.s(repr=False)
class RayCluster(Cluster):
    def setup(self):
        ray.init()

    def shutdown(self):
        ray.shutdown()

    def async_execute(
        self, execution: Execution, object_id_dict: typing.Dict[str, typing.Any]
    ) -> Execution:
        return execution.execute.remote(**object_id_dict)

    def execute(
        self, execution: Execution, object_id_dict: typing.Dict[str, typing.Any]
    ) -> typing.Any:
        return ray.get(execution.execute.remote(**object_id_dict))

    def execute_list(
        self,
        executions: typing.List[Execution],
        object_id_dicts: typing.List[typing.Dict[str, typing.Any]],
    ) -> typing.Any:
        pool = ActorPool(executions)
        return list(pool.map(lambda a, i: a.execute.remote(**i), object_id_dicts))

    def create_execution(
        self, execution_class: typing.Callable, *args, **kwargs
    ) -> Execution:
        return ray.remote(execution_class).remote(*args, **kwargs)

    def put(self, obj: typing.Any, name: str) -> typing.Dict[str, typing.Any]:
        object_id = ray.put(obj)
        self.cache[name] = object_id
        return {name: object_id}

    def get(self, name: str, object_id=None) -> typing.Any:
        if object_id is not None:
            return ray.get(object_id)
        return ray.get(self.cache[name])
