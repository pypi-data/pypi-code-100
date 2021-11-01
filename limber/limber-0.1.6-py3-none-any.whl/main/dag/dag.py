from typing import Optional
from datetime import timedelta
import inspect
from limber.imports.google import PubsubTopic, CloudSchedulerJob


class DAG:

    def __init__(self, dag_id: str, description: Optional[str], default_args: dict,
                 schedule_interval: [str, timedelta]):
        self.dag_id = dag_id
        self.description = description
        self.default_args = default_args
        self.schedule_interval = schedule_interval
        _, filename, line, function, _, _ = inspect.stack()[1]
        self.filename = filename

    def get_terraform_json(self, *, stack) -> {}:

        topic = PubsubTopic(
            stack,
            f"dag_{self.dag_id}",
            name=f"dag_{self.dag_id}"
        )

        CloudSchedulerJob(
            stack,
            f"job_{self.dag_id}",
            name=self.dag_id,
            description=self.description,
            schedule=self.schedule_interval,
            pubsub_target={
                "topic_name": topic.id,
                "data": "dGVzdA=="
            }
        )
