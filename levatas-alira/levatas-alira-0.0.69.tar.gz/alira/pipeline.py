import os
import logging
import yaml
import json
import sys
import importlib.util

from time import time
from uuid import uuid4

from importlib import import_module

from ml_metadata.metadata_store import metadata_store
from ml_metadata.proto.metadata_store_pb2 import (
    Execution,
    ExecutionType,
    Event,
    Artifact,
    ArtifactType,
    Attribution,
    Association,
    Context,
    ContextType,
    ParentContext,
    ConnectionConfig,
    INT,
    DOUBLE,
    STRING,
    STRUCT,
)
from ml_metadata.errors import NotFoundError


from alira.instance import Instance


PIPELINE_FILENAME = "pipeline.yml"
PIPELINE_PYTHON_FILENAME = "pipeline.py"


class Pipeline(object):

    ARTIFACT_PIPELINE_INPUT = "pipeline.input"
    ARTIFACT_PIPELINE_OUTPUT = "pipeline.output"
    ARTIFACT_MODULE_OUTPUT = "module.output"
    ARTIFACT_MODULE_INPUT = "module.input"

    ARTIFACT_TYPE_INSTANCE = "instance"
    CONTEXT_TYPE_PIPELINE = "pipeline"
    CONTEXT_TYPE_PIPELINE_EXECUTION = "pipeline.execution"

    METADATA_ARTIFACT_TYPE = "__metadata_artifact_type"
    METADATA_EXECUTION_NAME = "__metadata_execution_name"
    METADATA_PIPELINE_MODULE_NAME = "_pipeline_module_name"

    def __init__(
        self,
        pipeline_configuration: any = None,
        configuration_directory: str = None,
        store_configuration: dict = None,
        redis_server: str = None,
        aws_access_key: str = None,
        aws_secret_key: str = None,
        aws_region_name: str = None,
        **kwargs,
    ):
        self.kwargs = kwargs

        self.configuration_directory = configuration_directory or os.path.abspath(
            os.getcwd()
        )

        self.redis_server = redis_server
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key
        self.aws_region_name = aws_region_name

        # We are going to read the model identifier and the list of
        # modules from the pipeline.yml file.
        self.model_identifier = None
        self.modules = None

        self._load_pipeline_configuration(pipeline_configuration)
        self.pipeline_id = self._initialize_metadata_store(store_configuration)

    def run(self, data: dict) -> Instance:
        instance = Instance.create(data)

        pipeline_execution_context = self._create_pipeline_execution_context()
        self._create_instance_artifact(
            pipeline_execution_context.id, instance, Pipeline.ARTIFACT_PIPELINE_INPUT
        )

        for module in self.modules:
            if hasattr(module, Pipeline.METADATA_PIPELINE_MODULE_NAME):
                module_name = getattr(module, Pipeline.METADATA_PIPELINE_MODULE_NAME)
            else:
                module_name = f"{module.__module__}.{module.__class__.__name__}"

            input_artifact = self._create_instance_artifact(
                pipeline_execution_context.id, instance, Pipeline.ARTIFACT_MODULE_INPUT
            )

            module_execution = self._create_execution(
                pipeline_execution_context.id, module, module_name, input_artifact.id
            )

            output = module.run(instance=instance)
            if output is not None:
                output_key = (
                    f"{module_name}.{module.id}"
                    if hasattr(module, "id") and module.id is not None
                    else module_name
                )
                instance.properties[output_key] = output

            if output is not None and isinstance(output, dict):
                self._create_output_artifact(
                    pipeline_execution_context.id,
                    output,
                    module_name,
                    module_execution,
                )

        artifact = self._create_instance_artifact(
            pipeline_execution_context.id, instance, Pipeline.ARTIFACT_PIPELINE_OUTPUT
        )

        attribution = Attribution()
        attribution.artifact_id = artifact.id
        attribution.context_id = self.pipeline_id
        self.store.put_attributions_and_associations([attribution], [])

        return instance

    def _load_pipeline_configuration(self, pipeline_configuration):
        if pipeline_configuration is None:
            logging.info(
                "Configured a default pipeline since no specific configuration "
                "was specified."
            )
            self.model_identifier = "default"
            self.modules = []
            return

        if hasattr(pipeline_configuration, "read"):
            try:
                pipeline_configuration = yaml.safe_load(pipeline_configuration.read())
            except Exception as e:
                logging.exception(e)
                raise RuntimeError("Unable to load pipeline configuration")
        else:
            logging.info(
                f"Loading pipeline configuration from {pipeline_configuration}..."
            )

            try:
                with open(pipeline_configuration) as file:
                    pipeline_configuration = yaml.load(
                        file.read(), Loader=yaml.FullLoader
                    )
            except Exception as e:
                logging.exception(e)
                raise RuntimeError(
                    f"Unable to load pipeline configuration from file {pipeline_configuration}"
                )

        self.model_identifier = pipeline_configuration.get("name", None)
        if self.model_identifier is None:
            raise ValueError(
                "The name of the pipeline should be specified as part of "
                "the configuration."
            )

        self._load_pipeline_python_file()

        self.modules = []
        arguments = {
            "model_identifier": self.model_identifier,
            "configuration_directory": self.configuration_directory,
        }

        pipeline = pipeline_configuration.get("pipeline", [])

        # If the pipeline defines a set of AWS credentials, we want to overwrite the
        # credentials that were passed in.
        self.aws_access_key = pipeline_configuration.get(
            "aws_access_key", self.aws_access_key
        )
        self.aws_secret_key = pipeline_configuration.get(
            "aws_secret_key", self.aws_secret_key
        )
        self.aws_region_name = pipeline_configuration.get(
            "aws_region_name", self.aws_region_name
        )

        for module_configuration in pipeline:
            try:
                module_path, _, module_name = module_configuration["module"].rpartition(
                    "."
                )
                module = getattr(import_module(module_path), module_name)
                logging.info(f"Loaded module {module_path}.{module_name}")
            except ModuleNotFoundError as e:
                raise RuntimeError(
                    f"Unable to load module {module_path}.{module_name}"
                ) from e

            for argument_id, argument in module_configuration.items():
                if argument_id == "module":
                    continue

                arguments[argument_id] = argument

            arguments["redis_server"] = self.redis_server
            arguments["aws_access_key"] = self.aws_access_key
            arguments["aws_secret_key"] = self.aws_secret_key
            arguments["aws_region_name"] = self.aws_region_name

            arguments.update(self.kwargs)
            self.modules.append(module(**arguments))

    def _initialize_metadata_store(self, store_configuration: dict):
        connection_config = ConnectionConfig()

        if store_configuration is None:
            logging.info(
                "Metadata store is configured to work with an in-memory database."
            )
            connection_config.fake_database.SetInParent()
        elif "file" in store_configuration:
            logging.info("Metadata store is configured to work with a SQLite database.")
            connection_config.sqlite.filename_uri = store_configuration["file"]
            connection_config.sqlite.connection_mode = 3
        elif "host" in store_configuration:
            logging.info("Metadata store is configured to work with a MySQL database.")
            connection_config.mysql_database.host = store_configuration["host"]
            connection_config.mysql_database.port = store_configuration["port"]
            connection_config.mysql_database.user = store_configuration["user"]
            connection_config.mysql_database.password = store_configuration["password"]
            connection_config.mysql_database.database = store_configuration["database"]

        self.store = metadata_store.MetadataStore(connection_config)

        pipeline_id = None
        pipelines = self.store.get_contexts_by_type(
            type_name=Pipeline.CONTEXT_TYPE_PIPELINE
        )
        for pipeline in pipelines:
            if pipeline.name == self.model_identifier:
                pipeline_id = pipeline.id

        if pipeline_id is None:
            _log_message = f"{Pipeline.CONTEXT_TYPE_PIPELINE} context type"
            try:
                context_type_id = self.store.get_context_type(
                    type_name=Pipeline.CONTEXT_TYPE_PIPELINE
                ).id
                logging.info(f"Loaded {_log_message} {context_type_id}")
            except NotFoundError:
                context_type = ContextType()
                context_type.name = Pipeline.CONTEXT_TYPE_PIPELINE
                context_type.properties[Pipeline.CONTEXT_TYPE_PIPELINE] = 1
                context_type_id = self.store.put_context_type(context_type)
                logging.info(f"Created {_log_message} {context_type_id}")

            context = Context()
            context.type_id = context_type_id
            context.name = self.model_identifier
            pipeline_id = self.store.put_contexts([context])[0]

        return pipeline_id

    def _load_pipeline_python_file(self):
        python_filename = os.path.join(
            self.configuration_directory, PIPELINE_PYTHON_FILENAME
        )
        if os.path.isfile(python_filename):
            module_name = f"{self.model_identifier}.pipeline"

            try:
                spec = importlib.util.spec_from_file_location(
                    module_name, python_filename
                )
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)

                logging.info(f"Loaded {python_filename} as module {module_name}")
            except Exception as e:
                logging.exception(
                    f"There was an error loading {python_filename} as module {module_name}"
                )

    def _create_pipeline_execution_context(self):
        try:
            _log_message = (
                f"{Pipeline.CONTEXT_TYPE_PIPELINE_EXECUTION} pipeline execution context"
            )

            pipeline_execution_context_type = self.store.get_context_type(
                type_name=Pipeline.CONTEXT_TYPE_PIPELINE_EXECUTION
            )

            logging.info(f"Loaded {_log_message} {pipeline_execution_context_type.id}")
        except NotFoundError:
            pipeline_execution_context_type = ContextType()
            pipeline_execution_context_type.name = (
                Pipeline.CONTEXT_TYPE_PIPELINE_EXECUTION
            )
            pipeline_execution_context_type.properties[
                Pipeline.CONTEXT_TYPE_PIPELINE_EXECUTION
            ] = 1
            pipeline_execution_context_type.id = self.store.put_context_type(
                pipeline_execution_context_type
            )

            logging.info(f"Created {_log_message} {pipeline_execution_context_type.id}")

        pipeline_execution_context = Context()
        pipeline_execution_context.type_id = pipeline_execution_context_type.id
        pipeline_execution_context.name = (
            f"{self.model_identifier}.execution.{uuid4().hex}"
        )
        pipeline_execution_context.create_time_since_epoch = int(time() * 1000)

        pipeline_execution_context.id = self.store.put_contexts(
            [pipeline_execution_context]
        )[0]

        parent_context = ParentContext()
        parent_context.child_id = pipeline_execution_context.id
        parent_context.parent_id = self.pipeline_id
        self.store.put_parent_contexts([parent_context])

        return pipeline_execution_context

    def _create_execution(
        self, pipeline_execution_context_id, module, module_name, input_artifact_id
    ):
        try:
            _log_message = f"{module_name} execution type"

            module_execution_type = self.store.get_execution_type(type_name=module_name)

            logging.info(f"Loaded {_log_message} {module_execution_type.id}")
        except NotFoundError:
            module_execution_type = ExecutionType()
            module_execution_type.name = module_name
            module_execution_type.properties[Pipeline.METADATA_EXECUTION_NAME] = STRING

            for key, value in module.__dict__.items():
                if value is None:
                    continue

                module_execution_type.properties[key] = self._type(value)

            module_execution_type.id = self.store.put_execution_type(
                module_execution_type
            )

            logging.info(f"Created {_log_message} {module_execution_type.id}")

        module_execution = Execution()
        module_execution.type_id = module_execution_type.id
        module_execution.last_known_state = Execution.State.NEW
        module_execution.properties[
            Pipeline.METADATA_EXECUTION_NAME
        ].string_value = module_name

        for key, value in module.__dict__.items():
            if value is None:
                continue

            self._update_item(module_execution, key, value)

        module_execution.create_time_since_epoch = int(time() * 1000)
        module_execution_id = self.store.put_executions([module_execution])[0]
        module_execution.id = module_execution_id

        input_event = Event()
        input_event.artifact_id = input_artifact_id
        input_event.execution_id = module_execution.id
        input_event.type = Event.INPUT
        self.store.put_events([input_event])

        association = Association()
        association.execution_id = module_execution.id
        association.context_id = pipeline_execution_context_id

        self.store.put_attributions_and_associations([], [association])

        self._update_module_execution_state(module_execution, Execution.State.RUNNING)

        return module_execution

    def _create_instance_artifact(
        self, pipeline_execution_context_id, instance, metadata_uri
    ):
        try:
            _log_message = f"{Pipeline.ARTIFACT_TYPE_INSTANCE} artifact type"

            instance_artifact_type = self.store.get_artifact_type(
                type_name=Pipeline.ARTIFACT_TYPE_INSTANCE
            )

            logging.info(f"Loaded {_log_message} {instance_artifact_type.id}")
        except NotFoundError:
            instance_artifact_type = ArtifactType()
            instance_artifact_type.name = Pipeline.ARTIFACT_TYPE_INSTANCE
            instance_artifact_type.properties["prediction"] = INT
            instance_artifact_type.properties["confidence"] = DOUBLE
            instance_artifact_type.properties["image"] = STRING
            instance_artifact_type.properties["metadata"] = STRUCT
            instance_artifact_type.properties["properties"] = STRUCT
            instance_artifact_type.properties[Pipeline.METADATA_ARTIFACT_TYPE] = STRING

            instance_artifact_type.id = self.store.put_artifact_type(
                instance_artifact_type
            )

            logging.info(f"Created {_log_message} {instance_artifact_type.id}")

        return self._create_artifact(
            pipeline_execution_context_id,
            instance_artifact_type.id,
            instance,
            metadata_uri,
        )

    def _create_output_artifact(
        self, pipeline_execution_context_id, output, module_name, module_execution
    ):
        if not isinstance(output, dict):
            output = output.__dict__

        output[Pipeline.METADATA_ARTIFACT_TYPE] = module_name

        try:
            _log_message = f"{module_name} artifact type"

            output_artifact_type = self.store.get_artifact_type(type_name=module_name)

            logging.info(f"Loaded {_log_message} {output_artifact_type.id}")
        except NotFoundError:
            output_artifact_type = ArtifactType()
            output_artifact_type.name = module_name

            for key, value in output.items():
                if value is None:
                    continue

                output_artifact_type.properties[key] = self._type(value)

            output_artifact_type.id = self.store.put_artifact_type(output_artifact_type)

            logging.info(f"Created {_log_message} {output_artifact_type.id}")

        output_artifact = self._create_artifact(
            pipeline_execution_context_id,
            output_artifact_type.id,
            output,
            Pipeline.ARTIFACT_MODULE_OUTPUT,
        )

        output_event = Event()
        output_event.artifact_id = output_artifact.id
        output_event.execution_id = module_execution.id
        output_event.type = Event.OUTPUT
        self.store.put_events([output_event])

        self._update_module_execution_state(module_execution, Execution.State.COMPLETE)

        return output_artifact

    def _create_artifact(
        self, pipeline_execution_context_id, artifact_type_id, data, metadata_uri
    ):
        if not isinstance(data, dict):
            data = data.__dict__

        artifact = Artifact()
        artifact.type_id = artifact_type_id
        artifact.uri = metadata_uri

        for key, value in data.items():
            if value is None:
                continue

            self._update_item(artifact, key, value)

        artifact.create_time_since_epoch = int(time() * 1000)
        artifact.id = self.store.put_artifacts([artifact])[0]

        attribution = Attribution()
        attribution.artifact_id = artifact.id
        attribution.context_id = pipeline_execution_context_id
        self.store.put_attributions_and_associations([attribution], [])

        return artifact

    def _update_module_execution_state(self, module_execution, state):
        module_execution.last_known_state = state
        module_execution.last_update_time_since_epoch = int(time() * 1000)
        self.store.put_executions([module_execution])

    def _update_item(self, item, key, value):
        field_type = self._type(value)

        if field_type == STRING:
            if not isinstance(value, str):
                value = json.dumps(value, default=lambda o: "non-serializable")

            item.properties[key].string_value = value
        elif field_type == INT:
            item.properties[key].int_value = value
        elif field_type == DOUBLE:
            item.properties[key].double_value = value
        elif field_type == STRUCT and value:
            try:
                item.properties[key].struct_value.update(value)
            except ValueError:
                value = json.loads(json.dumps(value, default=lambda o: {}))
                item.properties[key].struct_value.update(value)

    def _type(self, value):
        field_type = type(value)
        if field_type is int:
            return INT

        if field_type is float:
            return DOUBLE

        if field_type is dict:
            return STRUCT

        return STRING
