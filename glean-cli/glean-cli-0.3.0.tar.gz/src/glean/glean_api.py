import os
import pathlib
import pkg_resources
from string import Template
from typing import Optional

import click
from click import ClickException
from requests import Session

from glean.credentials import CliCredentials

GLEAN_BASE_URI = os.environ.get("GLEAN_CLI_BASE_URI", default="https://glean.io")
VALID_FILE_EXTENSIONS = set([".json", ".yml"])
GLEAN_CLI_VERSION = pkg_resources.get_distribution("glean-cli").version


def login(session: Session, credentials: CliCredentials):
    """Authenticates the session with the provided credentials.

    :return The user's project ID, if successfully logged in.
    :raises ClickException if the login is not successful.
    """
    r = session.post(
        GLEAN_BASE_URI + "/auth/login-cli",
        data={
            "accessKeyId": credentials.access_key_id,
            "accessKeyToken": credentials.access_key_token,
        },
        headers={"Glean-CLI-Version": GLEAN_CLI_VERSION},
    )

    # TODO(dse): Show custom error message from server, if present.
    if r.status_code >= 500:
        raise ClickException("Unexpected error initiating your Glean session.")
    elif r.status_code >= 400:
        raise ClickException("Your access key is invalid.")
    if not r.ok:
        raise ClickException("Unexpected error initiating your Glean session.")

    return credentials.project_id


def create_build_from_git_revision(
    session: Session,
    project_id: str,
    git_revision: Optional[str],
    git_path: Optional[str],
    deploy: bool,
):
    """Creates a build based on a git revision and returns the result."""
    build_spec = {"configFilesFromGit": {"revision": git_revision, "path": git_path}}
    return _create_build(session, project_id, build_spec, deploy)


def create_build_from_local_files(
    session: Session, project_id: str, path: str, deploy: bool
):
    """Creates a build using local files and returns the result."""
    build_spec = _build_spec_from_local(path, project_id)
    return _create_build(session, project_id, build_spec, deploy)


def _create_build(session, project_id, build_spec, deploy):
    return _graphql_query(
        session,
        """
        mutation CreateBuild($projectId: String!, $buildSpec: BuildSpecInput!, $deploy: Boolean!) {
            createBuild( projectId: $projectId, buildSpec: $buildSpec, deploy: $deploy ) {
                id,
                resources {
                    added { models { name }, savedViews { name }, dashboards { name } }
                    updated { models { name }, savedViews { name }, dashboards { name } }
                    deleted { models { name }, savedViews { name }, dashboards { name } }
                },
                warnings,
                errors
            }
        }
        """,
        {
            "projectId": project_id,
            "buildSpec": build_spec,
            "deploy": deploy,
        },
    )


preview_uri = lambda build_results: click.style(
    f"{GLEAN_BASE_URI}/app/?build={build_results['data']['createBuild']['id']}",
    underline=True,
)

build_details_uri = lambda build_results: click.style(
    f"{GLEAN_BASE_URI}/app/p/builds/{build_results['data']['createBuild']['id']}",
    underline=True,
)


def _graphql_query(session: Session, query: str, variables: dict):
    r = session.post(
        GLEAN_BASE_URI + "/graphql/",
        json={"query": query, "variables": variables},
        headers={"Glean-CLI-Version": GLEAN_CLI_VERSION},
    )
    if r.status_code != 200:
        raise ClickException("Unexpected error received from the Glean server.")
    return r.json()


def _build_spec_from_local(path, project_id):
    # Maps parent_directory -> filename -> file contents
    inline_files = []
    for root, subdirs, filenames in os.walk(path):
        for filename in filenames:
            if pathlib.Path(filename).suffix not in VALID_FILE_EXTENSIONS:
                continue
            with open(os.path.join(root, filename), "r") as f:
                # Right now, changing the filepath of a config file changes its generated ID.
                # So, we set parentDirectory here to mimic the format that the server uses
                # when pulling from a git repo.
                parent_directory = root.replace(path, f"/tmp/repos/{project_id}")
                try:
                    file_contents = Template(f.read()).substitute(**os.environ)
                except KeyError as e:
                    raise ClickException(
                        f"No value found for environment variable substitution in {filename}: {str(e)}"
                    )

                inline_files.append(
                    {
                        "parentDirectory": parent_directory,
                        "filename": filename,
                        "fileContents": file_contents,
                    }
                )
    return {"inlineConfigFiles": inline_files}
