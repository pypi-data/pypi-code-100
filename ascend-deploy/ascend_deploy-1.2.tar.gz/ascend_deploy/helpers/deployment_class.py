from copy import deepcopy
import logging
import os
import sys
from importlib import import_module
from pathlib import Path
from typing import Union, List

import yaml
from ascend.sdk import definitions
from ascend.sdk.applier import DataflowApplier, ComponentApplier
from ascend.sdk.client import Client
from google.protobuf.json_format import MessageToJson


class dataflow_deployment:
    def __init__(
        self,
        path,                           # resource folder
        client: str,                    # client (instance)
        data_service_id: str,           # data service (target)
        dataflow_id: str,               # dataflow
        previous_data_service_id: str,  # data service (source)
        all_tags_mapping: dict,         # all_tags_mapping
    ) -> None:
        """
        :param path: Path to the dataflow folder, which contains the dataflow file with the same structure as you'd get with ascent.download_dataflow() function.
        :param data_service_id: The name of the environment, should be a key an available key config.yalm
        :param dataflow_id: The name of the dataflow which you want to apply functions to, and initialise and the likes.
        :param ascend_client: Pre-Initiated Ascend client.
        """



        # Local path
        self.dataflow_files_folder = path

        # Ascend details
        self.client = client
        self.data_service_id = data_service_id
        self.dataflow_id = dataflow_id
        self.previous_data_service_id = previous_data_service_id
        self.all_tags_mapping = all_tags_mapping

        # Ascend client
        self._init_client()

        self._init_paths()
        self._init_tags_mapping_config()
        self._init_dataflow_script_location()
        self._init_dataflow_objects()
        return

    def _init_paths(self):
        """
        Initiates paths which are used in other functions
        """
        self.current_folder = os.path.dirname(os.path.realpath(__file__))
        self.above_folder = os.path.join(os.path.dirname(__file__), "../../ascend")

    def _init_client(self) -> None:
    #    file_location = os.path.join(self.previous_data_service_id, "config.yaml")
    #    all_tags_mapping: dict = yaml.safe_load(open(file_location).read())

        access_key_id = self.all_tags_mapping['credentials'][self.client]['ascend_access_key_id']
        secret_access_key = self.all_tags_mapping['credentials'][self.client]['ascend_secret_access_key']

        self.ascend_client = Client('{}.ascend.io'.format(self.client), access_key_id, secret_access_key)
        return

    def _init_tags_mapping_config(self) -> None:
        """
        Starts the config.yaml file, which should be in the same directory as this.
        """

        #file_location = os.path.join(self.current_folder, "config.yaml")

        #all_tags_mapping: dict = yaml.safe_load(open(file_location).read())

        tagging_key = self.data_service_id #.lower()
        logging.debug(f"Getting the key {tagging_key} in the config.yaml file.")
        self.tags_mapping = self.all_tags_mapping.get(tagging_key, {})
        return

    def _init_dataflow_script_location(self) -> None:
        """
        Dynamically finds the Dataflow folder, assuming it is one layer above this file.
        """

        logging.info(
            f"Adding the folder {self.dataflow_files_folder} to the system path."
        )
        sys.path.append(self.dataflow_files_folder)

        dataflow_script_path = Path(
            f"{self.dataflow_files_folder}/{self.dataflow_id}.py"
        )

        logging.debug(
            f"Using the dynamically built path {dataflow_script_path} as the script location for this dataflow."
        )

        if os.path.isfile(dataflow_script_path) is False:
            raise Exception(
                f"Could not find the dataflow script at {dataflow_script_path}"
            )

    def _init_dataflow_objects(self) -> None:
        """
        Assuming you now have identified the dataflow folder, it imports the module in.
        """
        self.dataflow_objects = import_module(self.dataflow_id,)
        return

    ##########################################
    # TAG FUNCTIONS BELOW

    def update_feed_dataservice_connector(
        self, component: definitions.DataFeedConnector, value: str
    ) -> definitions.DataFeedConnector:
        component.input_data_service_id = value
        return component

    def update_writer_table_name(
        self,
        component: definitions.WriteConnector,
        replace_values: List[str],
        new_value: str,
    ) -> definitions.WriteConnector:
        print(component.container)
        for rv in replace_values:
            component.container.ms_sql_server.location_template = component.container.ms_sql_server.location_template.replace(
                rv, new_value
            )
        print(component.container)
        return component

    def update_azure_blob_prefix(
        self,
        component: definitions.WriteConnector,
        replace_values: List[str],
        new_value: str,
    ) -> definitions.WriteConnector:
        for rv in replace_values:
            print(rv)
#            component.container.abs.prefix = component.container.abs.prefix.replace(
            component.container.record_connection.connection_id.value = component.container.record_connection.connection_id.value.replace(
                rv, new_value
            )
        return component

    def update_refresh_frequency_reader(
        self, component: definitions.ReadConnector, value: int
    ) -> definitions.ReadConnector:
        if value > 1:
            component.update_periodical.period.seconds = value
        else:
            component.update_periodical = None
        return component

    # TAG FUNCTIONS ABOVE
    ##########################################

    def get_dataflow_class(self) -> None:
        """
        Gets the dataflow class, as created automatically by ascend into the dataflow.py file.
        """
        self.current_dataflow: definitions.Dataflow = getattr(
            self.dataflow_objects, f"dataflow_{self.dataflow_id}"
        )
        return

    def apply_functions_on_tags(self) -> None:
        applied_components = []
        for c in self.current_dataflow.components:
            for key in self.tags_mapping.keys():
                if key in c.description:
                    call_vars = {
                        k: v
                        for k, v in self.tags_mapping[key].items()
                        if k not in ["function_name"]
                    }
                    call_vars["component"] = c
                    c = getattr(self, self.tags_mapping[key]["function_name"])(
                        **call_vars
                    )
            applied_components.append(c)
        self.current_dataflow.components = applied_components

    def update_data_feed_connectors(self) -> None:
        """
        Updates the datafeed connectors to match the current `data_service_id`
        """
        # Get the current list of datafeed connectors
        datafeed_connectors: List[
            definitions.DataFeedConnector
        ] = self.current_dataflow.data_feed_connectors

        # Initiate an empty list to populate with the changes we want
        new_datafeed_connectors: List[definitions.DataFeedConnector] = []

        for dc in datafeed_connectors:
            # Logic for modifying it should be here
            # Currently only changing the data_service (E.G Test <-> Development)
            logging.debug(
                f"Changing the datafeed_connector {dc.name} `input_data_service_id` from {dc.input_data_service_id} to {self.data_service_id}."
            )
            dc.input_data_service_id = self.data_service_id
            new_datafeed_connectors.append(dc)

        self.current_dataflow.data_feed_connectors = new_datafeed_connectors
        return

    def get_all_readers(self) -> None:
        readers = [
            c
            for c in self.current_dataflow.components
            if isinstance(c, definitions.ReadConnector)
        ]
        [print(r.container) for r in readers]
        return

    def get_all_write_connectors(self) -> None:
        writers = [
            c
            for c in self.current_dataflow.components
            if isinstance(c, definitions.WriteConnector)
        ]
        mssql_components = [w for w in writers if w.container.HasField("ms_sql_server")]
        abs_components = [w for w in writers if w.container.HasField("abs")]
        return

    def print_components(self):
        """
        Print all the components found in the current_dataflow
        """
        for v in self.current_dataflow.components:
            print(v.id)
        print()

    def print_dataflow_connectors(self):
        """
        Print all the dataflow_connectors and their data_service_id found in the current_dataflow.
        """
        for v in self.current_dataflow.data_feed_connectors:
            print(v.id)
        return

    def get_component_dependecy(self, component_name) -> List[str]:
        """
        Gets all the dependencies of a component
        """
        dependencies_list = [component_name]
        temp_comp_list: List[definitions.Component] = [
            c for c in self.current_dataflow.components if c.id == component_name
        ]

        if len(temp_comp_list) == 0:
            return []

        temp_comp = temp_comp_list[0]

        for d in temp_comp.dependencies():
            dependencies_list.append(d)
            dependencies_list.extend(self.get_component_dependecy(d))

        return dependencies_list

    # def sort_components_on_dependency(self):
    #     """
    #     DOES NOT WORK
    #     """
    #     dataflow_dependency_order = {}
    #     for c in self.current_dataflow.components:
    #         dataflow_dependency_order[c] = self.get_component_dependecy(c.id)
    #     self.current_dataflow.components = list(
    #         dict(
    #             sorted(
    #                 dataflow_dependency_order.items(),
    #                 key=lambda i: -len(i[1]),
    #                 reverse=True,
    #             )
    #         ).keys()
    #     )
    #     return

    def create_connections(self):
        all_connections = self.ascend_client.list_connections(
            self.previous_data_service_id
        )

        for con in all_connections.data:
            try:
                self.ascend_client.get_connection(self.data_service_id,con.id.value)

            except Exception as e:
                #raise e
                self.ascend_client.share_connection(
                    self.previous_data_service_id, con.id.value, self.data_service_id)

                continue
        return

    def apply_components_list(self, cl):
        ca = ComponentApplier.build(
            client=self.ascend_client,
            data_service_id=self.data_service_id,
            dataflow_id=self.dataflow_id,
        )

        failed_components = []

        for cd in cl:
            print(cd.container.record_connection.connection_id.value)
            try:
                ca.apply(self.data_service_id, self.dataflow_id, cd)
            except Exception as e:
                failed_components.append(cd)

        if len(failed_components) > 0:
            print()
            print("Trying again")
            self.apply_components_list(cl)

        return

    def sort_components_on_dependency(self):
        """
        DOES NOT WORK
        """
        dataflow_dependency_order = {}
        for c in self.current_dataflow.components:
            dataflow_dependency_order[c] = self.get_component_dependecy(c.id)
        components_less_dependent = list(
            dict(
                sorted(
                    dataflow_dependency_order.items(),
                    key=lambda i: -len(i[1]),
                    reverse=True,
                )
            ).keys()
        )

        self.apply_components_list(components_less_dependent)

        return

    def apply_dataflow_on_ascend(
        self, temp_dataflow: definitions.Dataflow, remove_objects: bool = True
    ):
        """
        Creates the given dataflow, into the pre-established data_service
        """

        DataflowApplier(self.ascend_client).apply(
            dataflow=temp_dataflow,
            data_service_id=self.data_service_id,
            delete=remove_objects,
            dry_run=False,
        )

    def create_dataflow(self):
        """
        Applies the dataflow in full to ascend.
        Broken down because their API wouldn't do it, and this is just easier (even if messy as all hell.)
        """

        logging.warning(
            "BEFORE STARTING, MAKE SURE YOU HAVE THE RIGHT CREDENTIALS AND CONNECTIONS AVAILABLE ON THE DATA SERVICE."
        )

        self.create_connections()
        self.apply_dataflow_on_ascend(self.current_dataflow)
        exit()

if __name__ == "__main__":
    import deploy_functions as f

