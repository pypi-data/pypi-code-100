from pathlib import Path

import click

from dash_dashboards.commands.utils import valid_dir_name, validate_path_does_not_exist

from .config import DEFAULT_DASHBOARDS_DIR

BASE_APP_CONTENT = """from dash import Dash, Input, Output, html


layout = html.H1("Welcome to {dash_name}")

def callbacks(app: Dash):
    @app.callback(
        Output("output-id", "output_attribute"),
        [Input("input-id", "input_attribute")],
    )
    def callback_handler(input_attribute):
        output_attribute = html.H2("Callback output")
        return output_attribute
"""


@click.command(name="startdash")
@click.option("-n", "--name", prompt="Dashboard name", help="Dashboard name.")
@click.option(
    "-p",
    "--dash-dir-path",
    prompt="Dashboards directory",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    default=Path(DEFAULT_DASHBOARDS_DIR),
    help="Path to the dashboards directory",
)
def start_dash(name: str, dash_dir_path: Path):
    name = valid_dir_name(name)
    dash_path = dash_dir_path / name

    validate_path_does_not_exist(dash_path)
    dash_path.mkdir()

    init_path = dash_path / "__init__.py"
    init_path.touch()

    dash_app_path = dash_path / "app.py"
    with dash_app_path.open("w") as fp:
        fp.writelines(BASE_APP_CONTENT.format(dash_name=name))
