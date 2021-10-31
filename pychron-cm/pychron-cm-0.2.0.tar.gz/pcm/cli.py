# ===============================================================================
# Copyright 2021 ross
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================
import os
import shutil
import subprocess

import click
import platform

from pcm import render
from pcm import util
from pcm import requirements

IS_MAC = platform.system() == "Darwin"
IS_WINDOWS = platform.system() == "Windows"
HOME = os.path.expanduser("~")
EDM_ENVS_ROOT = os.path.join(HOME, ".edm", "envs")
EDM_BIN = os.path.join(EDM_ENVS_ROOT, "edm", "bin")

if IS_WINDOWS:
    GIT = "C:\\Git\\bin\\git"
else:
    GIT = "git"


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--template",
    default=None,
    help="Device Template to use. Typically the device models name",
)
@click.argument("name")
def device(template, name):
    click.echo("Create a new device configuration")


@cli.command()
@click.option(
    "--app",
    default="pycrunch",
    help="Application style to install. pycrunch, pyexperiment,...",
)
@click.option("--conda/--no-conda", default=False, help="Use Conda")
@click.option("--src/--no-src", "use_src", default=True, help="install the source code")
@click.option("--app_id", default=0, help="set the app id")
@click.option(
    "--fork", default="PychronLabsLLC", help="Name of the pychron fork to clone"
)
@click.option("--branch", default="dev/dr", help="Name of the pychron fork to clone")
@click.option(
    "--setupfiles/--no-setupfiles",
    "use_setupfiles",
    default=True,
    help="Install pychron setupfiles",
)
@click.option("--env", default="Pychron", help="Environment, aka root directory name")
@click.option(
    "--edm/--no-edm", "use_edm", default=True, help="Install the EDM environment"
)
@click.option("--environment", default="pychron", help="Name of the EDM environment")
@click.option(
    "--launcher/--no-launcher",
    "use_launcher",
    default=True,
    help="make a launcher script",
)
@click.option("--app_id", default=0, help="set the app id")
@click.option("--login/--no-login", default=0, help="show login window at startup")
@click.option(
    "--massspec_db_version", "msv", default=16, help="massspec database version"
)
@click.option(
    "--overwrite/--no-overwrite", default=False, help="Overwrite the file if it exists"
)
@click.option("--verbose/--no-verbose", default=False, help="Verbose output")
def wizard(
    app,
    conda,
    use_src,
    app_id,
    fork,
    branch,
    use_setupfiles,
    env,
    use_edm,
    environment,
    use_launcher,
    login,
    msv,
    overwrite,
    verbose,
):
    click.secho("Install the pychron application", bold="True", fg="green")
    if use_src:
        _code(fork, branch, app_id)

    if use_setupfiles:
        _setupfiles(env, overwrite, verbose)

    if use_edm:
        _edm(environment, verbose)

    if use_launcher:
        _launcher(
            conda, environment, app, fork, app_id, login, msv, None, overwrite, verbose
        )


@cli.command()
@click.option("--environment", default=None, help="Name of the EDM environment")
@click.option("--verbose/--no-verbose", default=False, help="Verbose output")
def edm(environment, verbose):
    _edm(environment, verbose)


def _edm(environment, verbose):
    click.secho("edm install", bold=True, fg="green")
    req = requirements.EDM_REQUIREMENTS
    cmdargs = ["edm", "install", "-y"] + req
    active_python = os.path.join(HOME, ".edm")
    if environment:
        active_python = os.path.join(
            active_python, "envs", environment, "bin", "python"
        )
        cmdargs.extend(["--environment", environment])
    else:
        active_python = os.path.join(active_python, "bin", "python")

    if verbose:
        click.echo(f'requirements: {" ".join(req)}')
        click.echo(f'command: {" ".join(cmdargs)}')
    subprocess.call(cmdargs)
    subprocess.call(
        [
            active_python,
            "-m",
            "pip",
            "install",
            "--no-dependencies",
            "uncertainties",
            "qimage2ndarray",
            "peakutils",
        ]
    )


@cli.command()
@click.option("--env", default="Pychron", help="Environment, aka root directory name")
@click.option(
    "--overwrite/--no-overwrite", default=False, help="Overwrite the file if it exists"
)
@click.option("--verbose/--no-verbose", default=False, help="Verbose output")
def setupfiles(env, overwrite, verbose):
    _setupfiles(env, overwrite, verbose)


def _setupfiles(env, overwrite, verbose):
    root = os.path.join(HOME, env)

    util.make_dir(root, "setupfiles")

    sf = os.path.join(root, "setupfiles")

    scripts = "scripts"
    util.make_dir(root, scripts)
    p = os.path.join(root, scripts, "defaults.yaml")
    util.write(p, render.render_template("defaults.yaml"), overwrite)

    measurement_args = "measurement", "unknown"
    extraction_args = "extraction", "extraction"
    procedure_args = "procedures", "procedure"

    for name, filename in (measurement_args, extraction_args, procedure_args):
        txt = render.render_template(filename)
        d = os.path.join(scripts, name)
        util.make_dir(root, d)
        p = os.path.join(root, d, "example_{}.py".format(filename))
        util.write(p, txt, overwrite)

    for d, ps in (
        ("canvas2D", ("canvas.yaml", "canvas_config.xml", "alt_config.xml")),
        ("extractionline", ("valves.yaml",)),
        ("monitors", ("system_monitor.cfg",)),
        ("", ("startup_tests.yaml", "experiment_defaults.yaml")),
    ):
        if d:
            out = os.path.join(sf, d)
            util.make_dir(sf, d)
        else:
            out = sf

        for template in ps:
            txt = render.render_template(template)
            p = os.path.join(out, template)
            util.write(p, txt, overwrite, verbose)

    ctx = {
        "canvas_path": os.path.join(sf, "canvas2D", "canvas.yaml"),
        "canvas_config_path": os.path.join(sf, "canvas2D", "canvas_config.xml"),
        "valves_path": os.path.join(sf, "extractionline", "valves.yaml"),
    }
    d = os.path.join(root, "preferences")
    util.make_dir(root, "preferences")
    p = os.path.join(d, "extractionline.ini")
    util.write(p, render.render_template("extractionline.ini", **ctx), overwrite)


@cli.command()
@click.option("--fork", help="Name of the pychron fork to clone")
@click.option("--branch", default="dev/dr", help="Name of the pychron fork to clone")
@click.option("--app_id", default=0, help="set the app id")
def code(fork, branch, app_id):
    _code(fork, branch, app_id)


def _code(fork, branch, app_id):
    update_root = os.path.join(HOME, f".pychron.{app_id}")
    ppath = os.path.join(update_root, "pychron")

    if not os.path.isdir(update_root):
        os.mkdir(update_root)

    if os.path.isdir(ppath):
        if not util.yes(
            "Pychron source code already exists. Remove and re-clone [y]/n"
        ):
            subprocess.call(["cd", ppath])
            subprocess.call([GIT, "status"])
            return

        shutil.rmtree(ppath)

    url = f"https://github.com/{fork}/pychron.git"

    subprocess.call([GIT, "clone", url, f"--branch={branch}", ppath])
    subprocess.call(["cd", ppath])
    subprocess.call([GIT, "status"])


@cli.command()
@click.option("--conda/--no-conda", default=False, help="Use the conda package manager")
@click.option("--environment", default="pychron", help="Python environment name")
@click.option("--app", default="pycrunch", help="application name")
@click.option("--org", default="PychronLabsLLC", help="Github organization")
@click.option("--app_id", default=0, help="set the app id")
@click.option("--login/--no-login", default=0, help="show login window at startup")
@click.option(
    "--massspec_db_version", "msv", default=16, help="massspec database version"
)
@click.option("--output", default="pychron_launcher.sh", help="Output path")
@click.option(
    "--overwrite/--no-overwrite", default=False, help="Overwrite the file if it exists"
)
@click.option("--verbose/--no-verbose", default=False, help="Verbose output")
def launcher(
    conda, environment, app, org, app_id, login, msv, output, overwrite, verbose
):
    _launcher(
        conda, environment, app, org, app_id, login, msv, output, overwrite, verbose
    )


def _launcher(
    conda, environment, app, org, app_id, login, msv, output, overwrite, verbose
):
    click.echo("launcher")
    template = "failed to make tmplate"
    if IS_MAC:
        if conda:
            template = "launcher_mac_conda"
        else:
            template = "launcher_mac"

    ctx = {
        "github_org": org,
        "app_name": app,
        "app_id": app_id,
        "use_login": login,
        "massspec_db_version": msv,
        "edm_envs_root": EDM_ENVS_ROOT,
        "edm_env": environment,
        "pychron_path": os.path.join(HOME, f".pychron.{app_id}", "pychron"),
    }

    txt = render.render_template(template, **ctx)

    if output is None:
        output = "pychron_launcher.sh"

    if verbose:
        click.echo(f"Writing launcher script: {output}")
        click.echo(txt)
    util.write(output, txt, overwrite)


@cli.command()
@click.option("--env", default="Pychron", help="Environment, aka root directory name")
@click.option(
    "--overwrite/--no-overwrite", default=False, help="Overwrite the file if it exists"
)
@click.option("--verbose/--no-verbose", default=False, help="Verbose output")
def init(env, overwrite, verbose):
    click.echo("make initialization file")
    template = "initialization.xml"
    txt = render.render_template(template)
    if verbose:
        click.echo("======== Initialization.xml contents start ========")
        click.echo(txt)
        click.echo("======== Initialization.xml contents end ========")

    root = os.path.join(HOME, env)
    sf = "setupfiles"
    util.make_dir(root, sf)

    p = os.path.join(root, sf, "initialization.xml")
    util.write(p, txt, overwrite=overwrite)


if __name__ == "__main__":
    cli()
# ============= EOF =============================================
