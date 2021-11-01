from typing import List

import click
from dagster_cloud.api.client import create_cloud_dagit_client

from ...cli.utils import add_options, create_cloud_dagit_client_options


@click.group(name="login")
def login_cli():
    """Customize your login settings."""


SET_ALLOWLISTED_DOMAINS_MUTATION = """
    mutation ($allowlistedDomains: [String!]) {
        setAllowlistedDomains(allowlistedDomains: $allowlistedDomains) {
            __typename
            ... on DagsterCloudOrganization {
                name
                allowlistedDomains
            }
            ... on PythonError {
                message
                stack
            }
        }
    }
    """


@login_cli.command(name="set-allowlisted-domains")
@add_options(create_cloud_dagit_client_options)
@click.option("--domain", "-d", "domains", type=click.STRING, required=True, multiple=True)
def set_allowlisted_domains_command(domains: List[str], url: str, api_token: str):
    """
    Configures an organization's allowed domains.

    After running this command, only new users with email addresses from the allowed domains will be
    able to authenticate into their organization's Dagster Cloud instance.

    If a user does not already have a Dagster Cloud account, but their email matches one of the
    allowed domains, an account is created on their behalf.
    """
    client = create_cloud_dagit_client(url, api_token)

    response = client.execute(
        SET_ALLOWLISTED_DOMAINS_MUTATION,
        variable_values={"allowlistedDomains": domains},
    )

    if response["data"]["setAllowlistedDomains"]["__typename"] == "DagsterCloudOrganization":
        click.echo(
            "Organization '{organization_name}' now has its allowlisted domains set to {domains}. "
            "Only users with email addresses from the allowed domains will be able to log into their "
            "organization's Dagster Cloud instance.".format(
                organization_name=response["data"]["setAllowlistedDomains"]["name"],
                domains=domains,
            )
        )
    else:
        raise click.ClickException(f"Error adding domains to allowlist: {response}")


@login_cli.command(name="clear-allowlisted-domains")
@add_options(create_cloud_dagit_client_options)
def clear_allowlisted_domains_command(url: str, api_token: str):
    """
    Removes all the allowed domains from an organization.

    After running this command, only users with email addresses corresponding to an existing
    Dagster Cloud account will be able to authenticate into their organization's
    Dagster Cloud instance.
    """
    client = create_cloud_dagit_client(url, api_token)

    response = client.execute(
        SET_ALLOWLISTED_DOMAINS_MUTATION,
        variable_values={"allowlistedDomains": []},
    )

    if response["data"]["setAllowlistedDomains"]["__typename"] == "DagsterCloudOrganization":
        click.echo(
            "Organization '{organization_name}' now has its allowlisted domains set to {domains}. "
        )
    else:
        raise click.ClickException(f"Error adding domains to allowlist: {response}")
