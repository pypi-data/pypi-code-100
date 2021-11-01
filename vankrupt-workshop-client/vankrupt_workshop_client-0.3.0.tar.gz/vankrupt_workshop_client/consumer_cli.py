import os
import pathlib
from dataclasses import asdict
from pprint import pprint

import appdirs
import click
from requests import HTTPError

from . import __version__, Auth
from .api import APIEnv
from .api.api_entities import GamingPlatform
from .api.consumer import ConsumerClient, ConsumerClientException

def_data_dir = pathlib.Path(appdirs.user_data_dir(
    appname='vankrupt_workshop_client',
    appauthor="vankrupt",
    version=__version__
))
def_config_dir = pathlib.Path(appdirs.user_config_dir(
    appname='vankrupt_workshop_client',
    appauthor="vankrupt",
    version=__version__
))
def_conf_path = pathlib.Path.joinpath(def_config_dir, 'store.')


@click.group()
@click.version_option(version=__version__)
@click.option(
    '--env', '-e',
    type=click.Choice([APIEnv.dev.value, APIEnv.release.value, APIEnv.local.value], case_sensitive=True),
    default=APIEnv.dev.value
)
@click.pass_context
def cli(ctx, env):
    """Vankrupt workshop uploader client"""
    enum_env = APIEnv(env)
    ctx.ensure_object(dict)

    conf_file = str(def_conf_path) + enum_env.value
    if not pathlib.Path(conf_file).is_file():
        ...
        # print('First, you need to run "init" against this environment')
    else:
        with open(conf_file, 'r') as f:
            mod_home_dir = pathlib.Path(f.read())
        ctx.obj['mod_home_dir'] = mod_home_dir

    client = ConsumerClient(env=enum_env)
    ctx.obj['client'] = client
    ctx.obj['conf_file'] = conf_file


@cli.command()
@click.option(
    '--mod_home_dir', '-d',
    type=click.Path(exists=True),
    required=False, default=None
)
@click.option(
    '--env', '-e',
    type=click.Choice([APIEnv.dev.value, APIEnv.release.value, APIEnv.local.value], case_sensitive=True),
    default=APIEnv.dev.value
)
def init(env, mod_home_dir):
    if mod_home_dir:
        mod_home_dir = pathlib.Path(mod_home_dir)
    else:
        mod_home_dir = def_data_dir

    conf_file = str(def_conf_path) + env
    print(f'Writing {mod_home_dir} to conf file: {conf_file}')
    with open(conf_file, 'w+') as f:
        f.write(str(mod_home_dir))


@cli.command()
@click.option(
    '--env', '-e',
    type=click.Choice([APIEnv.dev.value, APIEnv.release.value, APIEnv.local.value], case_sensitive=True),
    default=APIEnv.dev.value
)
def deinit(env):
    conf_file = str(def_conf_path) + env
    pathlib.Path(conf_file).unlink(missing_ok=True)


@cli.command()
@click.option(
    '--mod_id', '-mi',
    type=int,
    required=True
)
@click.pass_context
def inspect_mod(ctx, mod_id):
    client: ConsumerClient
    client = ctx.obj['client']
    try:
        mod = client.inspect_mod(mod_id=mod_id)
    except HTTPError as e:
        print("Error:")
        pprint(e.response.json())
    else:
        pprint(asdict(mod))


@cli.command()
@click.option(
    '--page', '-p',
    type=int,
    required=True
)
@click.option(
    '--platform', '-pl',
    required=True,
    type=click.Choice(
        [
            GamingPlatform.linux.value, GamingPlatform.windows.value,
            GamingPlatform.ps5.value, GamingPlatform.android
        ],
        case_sensitive=True
    ),
)
@click.pass_context
def filter_mods(ctx, page, platform):
    size = 5
    platform = GamingPlatform(platform)

    client: ConsumerClient
    client = ctx.obj['client']
    try:
        mod = client.filter_mods(page=page, platform=platform, size=size)
    except HTTPError as e:
        print("Error:")
        pprint(e.response.json())
    else:
        pprint(asdict(mod))


def init_file_related(ctx, platform) -> (ConsumerClient, GamingPlatform, str):
    if 'mod_home_dir' not in ctx.obj.keys():
        print('Please run "init" command first.')
        exit()
    else:
        mod_home_dir = ctx.obj['mod_home_dir']
        platform = GamingPlatform(platform) if platform else None
        client: ConsumerClient
        client = ctx.obj['client']
        return client, platform, mod_home_dir


@cli.command()
@click.option(
    '--mod_id', '-mi',
    type=int,
    required=True
)
@click.option(
    '--platform', '-pl',
    required=True,
    type=click.Choice(
        [
            GamingPlatform.linux.value, GamingPlatform.windows.value,
            GamingPlatform.ps5.value, GamingPlatform.android
        ],
        case_sensitive=True
    ),
)
@click.pass_context
def download(ctx, mod_id, platform):
    client, platform, mod_home_dir = init_file_related(ctx, platform=platform)
    try:
        print(f'Will be saving the mod to {mod_home_dir}')
        client.save_mod(mods_home_dir=mod_home_dir, platform=platform, mod_id=mod_id)
    except IsADirectoryError as e:
        print(e)
    except HTTPError as e:
        print("Error:")
        pprint(e.response.json())
    else:
        print("Done!")


@cli.command()
@click.option(
    '--mod_id', '-mi',
    type=int,
    required=True
)
@click.option(
    '--platform', '-pl',
    required=True,
    type=click.Choice(
        [
            GamingPlatform.linux.value, GamingPlatform.windows.value,
            GamingPlatform.ps5.value, GamingPlatform.android
        ],
        case_sensitive=True
    ),
)
@click.pass_context
def update(ctx, mod_id, platform):
    client, platform, mod_home_dir = init_file_related(ctx, platform=platform)
    try:
        print(f'Will update the mod from {mod_home_dir}')
        client.update_mod(mods_home_dir=mod_home_dir, platform=platform, mod_id=mod_id)
    except NotADirectoryError as e:
        print(e)
    except HTTPError as e:
        print("Error:")
        pprint(e.response.json())
    except (FileNotFoundError, ConsumerClientException) as e:
        print("Downloaded probably corrupted, delete and download again, might help")
        print(f"Original error: {e}")
    else:
        print("Done!")


@cli.command()
@click.option(
    '--mod_id', '-mi',
    type=int,
    required=True
)
@click.option(
    '--platform', '-pl',
    required=True,
    type=click.Choice(
        [
            GamingPlatform.linux.value, GamingPlatform.windows.value,
            GamingPlatform.ps5.value, GamingPlatform.android
        ],
        case_sensitive=True
    ),
)
@click.pass_context
def delete(ctx, mod_id, platform):
    client, platform, mod_home_dir = init_file_related(ctx, platform=platform)
    client.delete_mod(mods_home_dir=mod_home_dir, mod_id=mod_id, platform=platform)


@cli.command()
@click.pass_context
def list_downloaded(ctx):
    def get_immediate_subdirectories(a_dir):
        return [name for name in os.listdir(a_dir)
                if os.path.isdir(os.path.join(a_dir, name))]

    client, _, mod_home_dir = init_file_related(ctx, platform=None)
    dirs = get_immediate_subdirectories(mod_home_dir)
    print('Got folders of following mods: ')
    print(dirs)
