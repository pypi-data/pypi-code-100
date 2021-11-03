import json
from typing import Optional

import click
from box import Box

from montecarlodata.common.common import chunks
from montecarlodata.config import Config
from montecarlodata.errors import complain_and_abort, manage_errors, echo_error
from montecarlodata.queries.catalog import IMPORT_DBT_MANIFEST
from montecarlodata.utils import GqlWrapper


class DbtImportService:
    _IMPORT_NODES_BATCH_SIZE = 25

    def __init__(self,
                 config: Config,
                 dbt_manifest_file: str,
                 gql_wrapper: Optional[GqlWrapper] = None):
        self._gql_wrapper = gql_wrapper or GqlWrapper(mcd_id=config.mcd_id, mcd_token=config.mcd_token)
        with open(dbt_manifest_file, 'r') as f:
            self._dbt_manifest = Box(json.load(f))

    @manage_errors
    def import_dbt_manifest(self):
        try:
            dbt_schema_version = self._dbt_manifest.metadata.dbt_schema_version
            nodes = self._dbt_manifest.nodes
        except KeyError:
            complain_and_abort("Unexpected format of input file. Ensure that input file is a valid DBT manifest.json file")

        click.echo(f"\nImporting DBT objects into Monte Carlo catalog. please wait...")

        node_items = list(nodes.items())
        node_ids_imported = []
        bad_responses = []
        for nodes_items in chunks(node_items, self._IMPORT_NODES_BATCH_SIZE):
            response = self._gql_wrapper.make_request_v2(
                query=IMPORT_DBT_MANIFEST,
                operation='importDbtManifest',
                variables=dict(
                    dbtSchemaVersion=dbt_schema_version,
                    manifestNodesJson=json.dumps(dict(nodes_items))
                )
            )

            try:
                node_ids_imported.extend(response.data.response.nodeIdsImported)
            except KeyError:
                bad_responses.append(response)
                continue

        if bad_responses:
            echo_error("\nEncountered invalid responses.", bad_responses)

        click.echo(f"\nImported a total of {len(node_ids_imported)} DBT objects into Monte Carlo catalog.\n")

        return node_ids_imported