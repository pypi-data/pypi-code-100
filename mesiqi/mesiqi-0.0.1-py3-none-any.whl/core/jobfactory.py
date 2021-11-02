import os
from collections.abc import Set
from dataclasses import dataclass
from typing import List, Optional, Protocol, Type

import pandas as pd
from pydantic import BaseModel

from mesiqi.core import connector_factory, connector_loader
from mesiqi.core.connector import Connector
from mesiqi.core.logger import get_logger

logger = get_logger()


@dataclass
class Job:
    source: Connector
    sink: Connector
    config: dict

    def run(self):
        source = self.source
        sink = self.sink
        config = self.config
        iterator = source.read()
        for index, df in enumerate(iterator):
            res = sink.write(df)
            print(res)


@dataclass
class JobFactory:
    source_class: Type[Connector]
    sink_class: Type[Connector]
    config: dict

    def __call__(self) -> Job:
        source = self.source_class
        sink = self.sink_class
        config = self.config

        return Job(source, sink, config)


def run(job: Job) -> None:

    job.run()
