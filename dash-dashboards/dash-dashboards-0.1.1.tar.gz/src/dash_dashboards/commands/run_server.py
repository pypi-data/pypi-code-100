import click

from ..app import DashboardApp


@click.command(name="runserver")
@click.option("-h", "--host", type=str, default="127.0.0.1")
@click.option("-p", "--port", type=int, default=8000)
@click.option("-d", "--debug", default=False, is_flag=True)
@click.pass_obj
def run_server(app: DashboardApp, host: str, port: int, debug: bool):
    app.run_server(host=host, port=port, debug=debug)
