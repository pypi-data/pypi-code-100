"""CLI entrypoint 'matatika' command"""

import sys
from textwrap import dedent
import click
import pkg_resources
import auth0.v3.exceptions
import requests
from matatika.exceptions import MatatikaException

version = pkg_resources.require("matatika")[0].version


class ExceptionHandler(click.Group):
    """CLI entrypoint and error handling"""

    def invoke(self, ctx):
        """Invoke method override"""

        try:
            super().invoke(ctx)
            sys.exit(0)

        except MatatikaException as err:
            click.secho(str(err), fg='red')

        except auth0.v3.exceptions.Auth0Error as err:
            click.secho("Encountered an Auth0 error", fg='red')
            click.secho(str(err), fg='red')

        except requests.exceptions.HTTPError as err:

            msg = dedent(f"""\
                {repr(err)}
                
                Possible causes:
                \t- the authentication token may not be in the correct format (check it was copied correctly)
                \t- the authentication token may not be valid for the specified endpoint url
                \t- the authentication token may have expired
                """)

            click.secho(msg, fg='red')

        sys.exit(1)


@click.group(cls=ExceptionHandler)
@click.pass_context
@click.option("--auth-token", "-a", help="Authentication token")
@click.option("--client-id", "-i", help="Client ID")
@click.option("--client-secret", "-s", help="Client secret")
@click.option("--endpoint-url", "-e", help="Endpoint URL")
@click.option("--trace", "-t", is_flag=True, help="Trace variable sources")
@click.version_option(version=version)
def matatika(ctx, **kwargs):
    """CLI entrypoint and base command"""

    ctx.ensure_object(dict)
    ctx.obj.update(kwargs)
