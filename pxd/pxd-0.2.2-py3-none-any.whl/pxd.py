#   Copyright [2013-2021], Alibaba Group Holding Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import click

from deployer.config.config import setup_pxd_context, Config
from deployer.pxc.polardbx_manager import create_tryout_pxc, list_all_pxc, delete_pxc, cleanup_all_pxc, create_full_pxc, \
    print_pxd_version


@click.group()
def main():
    pass


@click.command(help='Create a minimum PolarDB-X cluster on local machine for tryout.')
@click.option("-name", default="pxc-tryout", help="PolarDB-X Cluster name, default: pxc-tryout")
@click.option("-cn_replica", default=1, help='cn node count')
@click.option("-cn_version", default="latest", help='cn node version')
@click.option("-dn_replica", default=1, help='dn node count')
@click.option("-dn_version", default="latest", help='dn node version')
@click.option("-cdc_replica", default=1, help='cdc node count')
@click.option("-cdc_version", default="latest", help='cdc node version')
@click.option("-repo", default="", help="docker repo url, default is docker hub")
def tryout(name, cn_replica, cn_version, dn_replica, dn_version, cdc_replica, cdc_version, repo):
    setup_pxd_context()
    Config.instance().load_config(CN_IMAGE_VERSION=cn_version, DN_IMAGE_VERSION=dn_version,
                                  CDC_IMAGE_VERSION=cdc_version, DOCKER_REPO_URL=repo)
    create_tryout_pxc(name, cn_replica, cn_version, dn_replica, dn_version, cdc_replica, cdc_version)


@click.command(help="Create a full PolarDB-X cluster on multi hosts.")
@click.option("-file", default=None, help='PolarDB-X cluster topology yaml file')
@click.option("-cn_version", default="latest", help='cn node version')
@click.option("-dn_version", default="latest", help='dn node version')
@click.option("-cdc_version", default="latest", help='cdc node version')
@click.option("-repo", default="", help="docker repo url, default is docker hub")
def create(file, cn_version, dn_version, cdc_version, repo):
    setup_pxd_context()
    Config.instance().load_config(CN_IMAGE_VERSION=cn_version, DN_IMAGE_VERSION=dn_version,
                                  CDC_IMAGE_VERSION=cdc_version, DOCKER_REPO_URL=repo)
    create_full_pxc(file, cn_version, dn_version, cdc_version)

@click.command(help="List PolarDB-X clusters.")
def list():
    setup_pxd_context()
    list_all_pxc()


@click.command(help="Clean up all PolarDB-X clusters.")
def cleanup():
    setup_pxd_context()
    cleanup_all_pxc()

@click.command(help="Delete specific PolarDB-X cluster.")
@click.argument("name", default=None)
def delete(name):
    setup_pxd_context()
    delete_pxc(name)

@click.command(help="Print pxd version.")
def version():
    print_pxd_version()


main.add_command(tryout)
main.add_command(create)
main.add_command(list)
main.add_command(cleanup)
main.add_command(delete)
main.add_command(version)

if __name__ == '__main__':
    main()
