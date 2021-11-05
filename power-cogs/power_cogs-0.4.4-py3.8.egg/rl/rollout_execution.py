import attr

# internal
from power_cogs.cluster.execution import Execution
from power_cogs.rl.agent import Agent
from power_cogs.rl.rollout import Rollout


@attr.s(repr=False)
class RolloutExecution(Execution):
    def rollout(self, agent: Agent, *args, **kwargs) -> Rollout:
        raise NotImplementedError("rollout method is not implemented!")

    def execute(self, *args, **kwargs) -> Rollout:
        return self.rollout(*args, **kwargs)
