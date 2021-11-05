# internal
from contextlib import contextmanager

from power_cogs.base.base import Base


class Agent(Base):
    def act(self, *args, **kwargs):
        raise NotImplementedError("act method not implemented!")

    @contextmanager
    def evaluate(self):
        try:
            yield
        finally:
            pass
