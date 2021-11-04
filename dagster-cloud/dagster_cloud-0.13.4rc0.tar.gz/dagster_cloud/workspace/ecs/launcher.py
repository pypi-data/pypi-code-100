import uuid
from typing import Any, Dict, Iterable, List, Optional

import boto3
import botocore
from dagster import Array, Field, check
from dagster.core.host_representation.grpc_server_registry import GrpcServerEndpoint
from dagster.core.launcher import RunLauncher
from dagster.serdes import ConfigurableClass, ConfigurableClassData
from dagster_aws.ecs import EcsRunLauncher
from dagster_cloud.workspace.origin import CodeDeploymentMetadata

from ..user_code_launcher import ReconcileUserCodeLauncher

EcsServerHandleType = str


class EcsUserCodeLauncher(ReconcileUserCodeLauncher[EcsServerHandleType], ConfigurableClass):
    def __init__(
        self,
        cluster: str,
        subnets: List[str],
        execution_role_arn: str,
        log_group: str,
        service_discovery_namespace_id: str,
        inst_data: Optional[ConfigurableClassData] = None,
    ):
        self.ecs = boto3.client("ecs")
        self.logs = boto3.client("logs")
        self.service_discovery = boto3.client("servicediscovery")

        # TODO: Default to default cluster
        self.cluster = cluster
        # TODO: Default to default networking
        self.subnets = subnets
        self.service_discovery_namespace_id = service_discovery_namespace_id
        # TODO: Create a role if one doesn't exist?
        self.execution_role_arn = execution_role_arn
        # TODO: Create a log group if one doesn't exist?
        self.log_group = log_group
        self._inst_data = check.opt_inst_param(inst_data, "inst_data", ConfigurableClassData)
        super(EcsUserCodeLauncher, self).__init__()

    @property
    def requires_images(self):
        return True

    @classmethod
    def config_type(cls):
        return {
            "cluster": Field(str),
            "subnets": Field(Array(str)),
            "execution_role_arn": Field(str),
            "log_group": Field(str),
            "service_discovery_namespace_id": Field(str),
        }

    @staticmethod
    def from_config_value(inst_data: ConfigurableClassData, config_value: Dict[str, Any]):
        return EcsUserCodeLauncher(inst_data=inst_data, **config_value)

    @property
    def inst_data(self) -> ConfigurableClassData:
        return self._inst_data

    def _create_new_server_endpoint(
        self, location_name: str, metadata: CodeDeploymentMetadata
    ) -> GrpcServerEndpoint:
        server_name = uuid.uuid4().hex
        port = 4000

        # https://docs.aws.amazon.com/AmazonECS/latest/developerguide/create-service-discovery.html
        service_registry_arn = (
            self.service_discovery.create_service(
                Name=server_name,
                NamespaceId=self.service_discovery_namespace_id,
                DnsConfig={
                    "DnsRecords": [
                        {"Type": "A", "TTL": 60},
                    ]
                },
            )
            .get("Service", {})
            .get("Arn")
        )

        # TODO: Upsert task definitions
        python_env = (
            {"name": "DAGSTER_CLI_API_GRPC_PYTHON_FILE", "value": metadata.python_file}
            if metadata.python_file
            else {"name": "DAGSTER_CLI_API_GRPC_PACKAGE_NAME", "value": metadata.package_name}
        )
        task_definition_arn = (
            self.ecs.register_task_definition(
                family=location_name,
                requiresCompatibilities=["FARGATE"],
                networkMode="awsvpc",
                containerDefinitions=[
                    {
                        "name": "server",
                        "image": metadata.image,
                        "environment": [
                            {"name": "DAGSTER_CURRENT_IMAGE", "value": metadata.image},
                            python_env,
                        ],
                        "command": [
                            "dagster",
                            "api",
                            "grpc",
                            "-p",
                            str(port),
                            "-h",
                            "0.0.0.0",
                            "--lazy-load-user-code",
                        ],
                        "logConfiguration": {
                            "logDriver": "awslogs",
                            "options": {
                                "awslogs-group": self.log_group,
                                "awslogs-region": self.ecs.meta.region_name,
                                "awslogs-stream-prefix": location_name,
                            },
                        },
                    },
                ],
                executionRoleArn=self.execution_role_arn,
                # TODO: Configurable
                # https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-cpu-memory-error.html
                cpu="256",
                memory="512",
            )
            .get("taskDefinition")
            .get("taskDefinitionArn")
        )

        self.ecs.create_service(
            cluster=self.cluster,
            serviceName=server_name,
            taskDefinition=task_definition_arn,
            desiredCount=1,
            networkConfiguration={
                "awsvpcConfiguration": {
                    "subnets": self.subnets,
                    # TODO: Choose proper public IP strategy:
                    # https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_cannot_pull_image.html
                    "assignPublicIp": "ENABLED",
                },
            },
            serviceRegistries=[
                {"registryArn": service_registry_arn},
            ],
            tags=[
                {"key": "dagster/location_name", "value": location_name},
            ],
        )

        self._poll_service_start(server_name)

        namespace = (
            self.service_discovery.get_namespace(
                Id=self.service_discovery_namespace_id,
            )
            .get("Namespace")
            .get("Name")
        )
        host = f"{server_name}.{namespace}"
        server_id = self._wait_for_server(host=host, port=4000, timeout=60)

        endpoint = GrpcServerEndpoint(
            server_id=server_id,
            host=host,
            port=port,
            socket=None,
        )
        return endpoint

    def _remove_server_handle(self, server_handle: EcsServerHandleType) -> None:
        self.ecs.update_service(cluster=self.cluster, service=server_handle, desiredCount=0)
        self.ecs.get_waiter("services_stable").wait(cluster=self.cluster, services=[server_handle])
        self.ecs.delete_service(cluster=self.cluster, service=server_handle)
        self.ecs.get_waiter("services_inactive").wait(
            cluster=self.cluster, services=[server_handle]
        )

    def _get_server_handles_for_location(self, location_name: str) -> Iterable[EcsServerHandleType]:
        handles = []
        paginator = self.ecs.get_paginator("list_services")
        for page in paginator.paginate(cluster=self.cluster):
            for arn in page.get("serviceArns"):
                tags = self.ecs.list_tags_for_resource(resourceArn=arn).get("tags", {})
                location_names = [
                    tag.get("value") for tag in tags if tag.get("key") == "dagster/location_name"
                ]
                if location_name in location_names:
                    handles.append(arn)
        return handles

    def _cleanup_servers(self):
        paginator = self.ecs.get_paginator("list_services")
        for page in paginator.paginate(cluster=self.cluster):
            for arn in page.get("serviceArns"):
                tags = self.ecs.list_tags_for_resource(resourceArn=arn).get("tags", {})
                tag_keys = [tag.get("key") for tag in tags]
                if "dagster/location_name" in tag_keys:
                    self._remove_server_handle(arn)

    def get_step_handler(self, _execution_config):
        pass

    def run_launcher(self) -> RunLauncher:
        launcher = EcsRunLauncher()
        launcher.register_instance(self._instance)

        return launcher

    def _poll_service_start(self, service_name: str) -> None:
        # Check if we can place a task; this is fairly quick
        # TODO: handle IAM eventual consistency; sometimes the first event will
        # read "ECS was unable to assume the role" but will resolve itself with
        # enough time:
        # https://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_general.html#troubleshoot_general_eventual-consistency
        try:
            self.ecs.get_waiter("services_stable").wait(
                cluster=self.cluster,
                services=[service_name],
                # 5 minutes
                WaiterConfig={
                    "Delay": 2,
                    "MaxAttempts": 150,
                },
            )

        except botocore.exceptions.WaiterError:
            service = self.ecs.describe_services(
                cluster=self.cluster,
                services=[service_name],
            ).get("services")[0]

            messages = [event.get("message") for event in service.get("events")]

            # These strings in event messages indicate we couldn't create a task
            # https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-event-messages.html#service-event-messages-list
            failures = ["unable", "unhealthy", "throttled"]
            for message in messages:
                if any(failure in message for failure in failures):
                    # TODO: Custom exception
                    raise Exception(messages)

        self._poll_tasks_start(service_name)

    def _poll_tasks_start(self, service_name: str) -> None:
        # Check if a task can start; this is pretty slow but
        # will return very quickly on the happy path
        # TODO: Can we make it fail faster if it can't pull the image?
        try:
            self.ecs.get_waiter("services_stable").wait(
                cluster=self.cluster,
                services=[service_name],
                # 5 minutes
                WaiterConfig={
                    "Delay": 1,
                    "MaxAttempts": 300,
                },
            )

        except botocore.exceptions.WaiterError:
            task_arns = self.ecs.list_tasks(
                cluster=self.cluster,
                serviceName=service_name,
                desiredStatus="STOPPED",
            ).get("taskArns")
            tasks = self.ecs.describe_tasks(cluster=self.cluster, tasks=task_arns).get("tasks")
            reasons = [task.get("stoppedReason") for task in tasks]
            raise Exception(reasons)

        self._poll_tasks_running(service_name)

    def _poll_tasks_running(self, service_name: str) -> None:
        # Get the list of running tasks:
        task_arns = self.ecs.list_tasks(
            cluster=self.cluster,
            serviceName=service_name,
            desiredStatus="RUNNING",
        ).get("taskArns")

        # Poll to see if they stop:
        # TODO: don't introduce this delay to the happy path
        try:
            self.ecs.get_waiter("tasks_stopped").wait(
                cluster=self.cluster,
                tasks=task_arns,
                # 1 minute
                WaiterConfig={
                    "Delay": 1,
                    "MaxAttempts": 60,
                },
            )

        # If they don't, conclude that they're healthy
        # and return early:
        except botocore.exceptions.WaiterError:
            return

        # If they stop, raise their logs:
        task_arns = self.ecs.list_tasks(
            cluster=self.cluster,
            serviceName=service_name,
            desiredStatus="STOPPED",
        ).get("taskArns")

        raise Exception(self._get_logs(task_arns[0]))

    def _get_logs(self, task_arn: str) -> List[str]:
        task_id = task_arn.split("/")[-1]

        task = self.ecs.describe_tasks(cluster=self.cluster, tasks=[task_arn],).get(
            "tasks"
        )[0]
        task_definition = self.ecs.describe_task_definition(
            taskDefinition=task.get("taskDefinitionArn"),
        ).get("taskDefinition")
        container = task_definition.get("containerDefinitions")[0]
        container_name = container.get("name")
        log_stream_prefix = (
            container.get("logConfiguration", {}).get("options", {}).get("awslogs-stream-prefix")
        )

        log_stream = f"{log_stream_prefix}/{container_name}/{task_id}"

        events = self.logs.get_log_events(
            logGroupName=self.log_group,
            logStreamName=log_stream,
        ).get("events")

        return [event.get("message") for event in events]
