# pylint: disable=too-few-public-methods,too-many-arguments

"""CLI utilities"""

from typing import Dict, Tuple
import click
from matatika.cli.display import Column, Table
from matatika.library import MatatikaClient
from matatika.cli.variables import (
    AuthTokenVariable,
    BaseVariable,
    ClientIdVariable,
    ClientSecretVariable,
    EndpointUrlVariable,
    VariableSource,
    VariableType,
    WorkspaceIdVariable
)
from matatika.exceptions import VariableNotSetError


class Resolver():
    """Resolves values from from click commands and the context file"""

    def __init__(self, ctx):
        self.ctx = ctx

    def _resolve(self, **variables: BaseVariable) -> Dict[str, Tuple[str, VariableSource]]:
        resolved_variables = {name: variable().get(
            self.ctx) for name, variable in variables.items() if variable}

        auth_token_value = resolved_variables[VariableType.AUTH_TOKEN.value][0]
        client_id_value = resolved_variables[VariableType.CLIENT_ID.value][0]
        client_secret_value = resolved_variables[VariableType.CLIENT_SECRET.value][0]

        for name, (value, _source) in resolved_variables.items():
            if not value:
                if name is VariableType.AUTH_TOKEN.value:
                    if client_id_value or client_secret_value:
                        continue

                elif name is VariableType.CLIENT_ID.value:
                    if auth_token_value:
                        continue

                elif name is VariableType.CLIENT_SECRET.value:
                    if auth_token_value:
                        continue

                raise VariableNotSetError(VariableType(name).name)

        return resolved_variables

    def client(self,
               auth_token=AuthTokenVariable,
               client_id=ClientIdVariable,
               client_secret=ClientSecretVariable,
               endpoint_url=EndpointUrlVariable,
               workspace_id=WorkspaceIdVariable
               ) -> MatatikaClient:
        """Returns a MatatikaClient object populated with resolved values"""

        variables = self._resolve(auth_token=auth_token,
                                  client_id=client_id,
                                  client_secret=client_secret,
                                  endpoint_url=endpoint_url,
                                  workspace_id=workspace_id)

        if self.ctx.obj['trace']:
            names = Column("VARIABLE NAME")
            values = Column("VALUE")
            sources = Column("SOURCE")

            for name, (value, source) in variables.items():
                names.add(name)
                values.add(value)
                sources.add(source.value if source else "N/A")

            table = Table(names, values, sources)

            click.echo("Creating a client with the following variables...\n")
            click.echo(table)
            click.echo()

        # filter out source
        variables = {name: value for name,
                     (value, _source) in variables.items()}

        client = MatatikaClient(**variables)
        client._from_cli = True  # pylint: disable=protected-access
        return client
