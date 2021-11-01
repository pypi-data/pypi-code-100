import json
import os
import pathlib
from dataclasses import asdict
from pprint import pprint

import appdirs
import click
from dacite import from_dict
from requests import HTTPError

from . import __version__, Auth
from .api import APIEnv
from .api.api_entities import ModCreate, ModFileUploadRequest, GamingPlatform
from .api.creator import CreatorClient, AuthError

def_config_dir = appdirs.user_config_dir(
    appname='vankrupt_workshop_client',
    appauthor="vankrupt",
    version=__version__
)
def_auth_path = pathlib.Path.joinpath(pathlib.Path(def_config_dir), 'auth.')


def rewrite_auth(client: CreatorClient):
    root = def_auth_path.parent
    pathlib.Path.mkdir(root, parents=True, exist_ok=True)
    conf_file = str(def_auth_path) + client.env.value
    with open(conf_file, 'w+') as config_f:
        a = Auth(access_token=client._access_token, refresh_token=client._refresh_token, env=client.env.value)
        s = json.dumps(asdict(a))
        config_f.write(s)


def delete_auth(client: CreatorClient):
    conf_file = str(def_auth_path) + client.env.value
    pathlib.Path.unlink(pathlib.Path(conf_file), missing_ok=True)


@click.group()
@click.version_option(version=__version__)
@click.option(
    '--config_store', '-c',
    type=click.File('rb'),
    default=None
)
@click.option(
    '--env', '-e',
    type=click.Choice([APIEnv.dev.value, APIEnv.release.value, APIEnv.local.value], case_sensitive=True),
    default=APIEnv.dev.value
)
@click.pass_context
def cli(ctx, config_store, env):
    """Vankrupt workshop uploader client"""
    enum_env = APIEnv(env)
    # try to read auth configs
    client = CreatorClient(env=enum_env)
    try:
        conf_file = str(def_auth_path) + enum_env.value
        if not config_store:
            config_store = open(conf_file, 'r')

        c_s = config_store.read()
        c_d = json.loads(c_s)
        auth_l = from_dict(data_class=Auth, data=c_d)
    except Exception as e:
        print(e)
    else:
        client._authenticate(a_t=auth_l.access_token, r_t=auth_l.refresh_token)

    ctx.ensure_object(dict)
    ctx.obj['client'] = client


@cli.command()
@click.option(
    '--string', '-s'
)
def echo(string):
    print(string)


@cli.command()
@click.option(
    '--email', '-e',
    prompt=True,
)
@click.option(
    "--password", '-p',
    prompt=True,
    hide_input=True,
)
@click.pass_context
def login(ctx, email, password):
    client: CreatorClient
    client = ctx.obj['client']
    try:
        client.authenticate(username=email, password=password)
    except Exception as e:
        print("Authentication failed")
        return
    print(f'Saving configs to root {def_auth_path.parent}')
    rewrite_auth(client=client)


@cli.command()
def logout(ctx):
    client: CreatorClient
    client = ctx.obj['client']
    delete_auth(client)


@cli.command()
@click.pass_context
def get_me(ctx):
    client: CreatorClient
    client = ctx.obj['client']
    if not client.authenticated:
        print("Unauthenticated, authenticate first.")
        return
    try:
        me = client.get_me()
        pprint(asdict(me), sort_dicts=False)
    except Exception as e:
        print('Got error:')
        raise e
    else:
        rewrite_auth(client)


@cli.command()
@click.option(
    '--name', '-n',
    required=True
)
@click.option(
    '--description', '-d',
    required=True
)
@click.pass_context
def create_mod(ctx, name, description):
    client: CreatorClient
    client = ctx.obj['client']
    if not client.authenticated:
        print("Unauthenticated, authenticate first.")
        return
    try:
        mod = client.create_mod(mod=ModCreate(name=name, description=description))
        pprint(asdict(mod), sort_dicts=False)
    except HTTPError as e:
        print('Got error:')
        pprint(e.response.json())
    except AuthError:
        print('Got auth error, logging out')
        delete_auth(client)
    else:
        rewrite_auth(client)


@cli.command()
@click.option(
    '--mod_id', '-mi',
    required=True
)
@click.option(
    '--platform', '-p',
    required=True,
    type=click.Choice(
        [
            GamingPlatform.linux.value, GamingPlatform.windows.value,
            GamingPlatform.ps5.value, GamingPlatform.android
        ],
        case_sensitive=True
    ),
)
@click.option(
    '--update_message', '-um',
    required=True
)
@click.option(
    '--file_path', '-f',
    type=click.Path(exists=True),
    required=True
)
@click.option(
    '--size', '-s',
    type=int,
    default=None
)
@click.pass_context
def upload(ctx, mod_id, platform, update_message, file_path, size):
    if not pathlib.Path(file_path).is_file():
        print("Not a file!")
        return
    real_size = os.path.getsize(file_path)
    if not size:
        size = real_size
    elif size > real_size:
        print(f"{file_path} is too small, it does not have {size} bytes")
        return

    client: CreatorClient
    client = ctx.obj['client']
    if not client.authenticated:
        print("Unauthenticated, authenticate first.")
        return

    try:
        new_v = ModFileUploadRequest(platform=GamingPlatform(platform), update_message=update_message, size=size)
        upl = client.initiate_upload(mod_id=mod_id, mod_version=new_v)
        pprint(upl)
        print("\n\n")
        print("Beginning uploading!")
        with open(file_path, 'rb') as f:
            bytes_to_send = f.read(size)

        resp = client.upload_mod(mod_size=size, mod_file=bytes_to_send, policy_document=upl.signed_policy)
        if resp.status_code == 204:
            print("Success!")

    except HTTPError as e:
        print('Got error:')
        pprint(e.response.json())
    except AuthError:
        print('Got auth error, logging out')
        delete_auth(client)
    else:
        rewrite_auth(client)
