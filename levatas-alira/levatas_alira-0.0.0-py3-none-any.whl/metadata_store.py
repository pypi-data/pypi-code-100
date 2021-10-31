from ml_metadata.metadata_store import metadata_store
from ml_metadata.proto import metadata_store_pb2
from ml_metadata.errors import NotFoundError


FAKE = 'FAKE'
MYSQL = 'MYSQL'
SQLITE = 'SQLite'


class MetadataStoreFactory:
    
    @staticmethod
    def create_metadata_store(database_engine: str = SQLITE, configuration: dict = {}):
        if database_engine == SQLITE:
            connection_config = metadata_store_pb2.ConnectionConfig()
            connection_config.sqlite.filename_uri = configuration["DATABASE_FILE"]
            connection_config.sqlite.connection_mode = 3
            return metadata_store.MetadataStore(connection_config)

        if database_engine == MYSQL:
            connection_config = metadata_store_pb2.ConnectionConfig()
            connection_config.mysql.host = configuration["DATABASE_HOST"]
            connection_config.mysql.port = configuration["DATABASE_PORT"]
            connection_config.mysql.database = configuration["DATABASE_NAME"]
            connection_config.mysql.user = configuration["DATABASE_USER"]
            connection_config.mysql.password = configuration["DATABASE_PASSWORD"]
            return metadata_store.MetadataStore(connection_config)

        connection_config = metadata_store_pb2.ConnectionConfig()
        connection_config.fake_database.SetInParent()
        return metadata_store.MetadataStore(connection_config)

    @staticmethod
    def initialize_metadata_entity_types(store):
        entity_types = {}

        try:
            workflow_type = store.get_context_type(type_name="Pipeline")
            entity_types["_pipeline_type"] = workflow_type.id
        except NotFoundError:
            workflow_context_type = metadata_store_pb2.ContextType()
            workflow_context_type.name = "Pipeline"
            entity_types["_pipeline_type"] = store.put_context_type(workflow_context_type)

        try:
            component_execution_type = store.get_execution_type(type_name="Component")
            entity_types["_component_type"] = component_execution_type.id
        except NotFoundError:
            component_execution_type = metadata_store_pb2.ExecutionType()
            component_execution_type.name = "Component"
            component_execution_type.properties["name"] = metadata_store_pb2.STRING
            entity_types["_component_type"] = store.put_execution_type(component_execution_type)

        try:
            workflow_type = store.get_context_type(type_name="PipelineExecution")
            entity_types["_pipeline_execution_type"] = workflow_type.id
        except NotFoundError:
            workflow_context_type = metadata_store_pb2.ContextType()
            workflow_context_type.name = "PipelineExecution"
            entity_types["_pipeline_execution_type"] = store.put_context_type(workflow_context_type)
        
        try:
            instance_type = store.get_artifact_type(type_name="Instance")
            entity_types["_instance_type"] = instance_type.id
        except NotFoundError:
            instance_type = metadata_store_pb2.ArtifactType()
            instance_type.name = "Instance"
            instance_type.properties["classification"] = metadata_store_pb2.INT
            instance_type.properties["confidence"] = metadata_store_pb2.DOUBLE
            instance_type.properties["metadata"] = metadata_store_pb2.STRUCT
            entity_types["_instance_type"] = store.put_artifact_type(instance_type)

        try:
            result_type = store.get_artifact_type(type_name="ComponentInput")
            entity_types["_component_input_type"] = result_type.id
        except NotFoundError:
            result_type = metadata_store_pb2.ArtifactType()
            result_type.name = "ComponentInput"
            result_type.properties["instance"] = metadata_store_pb2.STRUCT
            entity_types["_component_input_type"] = store.put_artifact_type(result_type)

        try:
            result_type = store.get_artifact_type(type_name="ComponentResult")
            entity_types["_component_result_type"] = result_type.id
        except NotFoundError:
            result_type = metadata_store_pb2.ArtifactType()
            result_type.name = "ComponentResult"
            result_type.properties["metadata"] = metadata_store_pb2.STRUCT
            entity_types["_component_result_type"] = store.put_artifact_type(result_type)

        return entity_types

    def initialize_pipeline_metadata(pipeline_name, pipeline_type_id, store):
        pipelines = store.get_contexts_by_type(type_name="Pipeline")
        for pipeline in pipelines:
            if pipeline.name == pipeline_name:
                return pipeline.id

        context = metadata_store_pb2.Context()
        context.type_id = pipeline_type_id
        context.name = pipeline_name

        return store.put_contexts([context])[0]