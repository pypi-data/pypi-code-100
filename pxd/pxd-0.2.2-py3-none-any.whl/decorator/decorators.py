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

import functools
import logging

import click

from deployer.util.sqlite_manager import SQLiteManager

logger = logging.getLogger(__name__)

def pxc_create_task(task_name="DEFAULT"):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            pxc = args[0]
            try:
                logger.info('task_name: %s, call %s():', task_name, func.__name__)
                click.echo('    ' + task_name)
                ret = func(*args, **kw)
                update_polardbx_record(pxc)
                return ret
            except Exception as ex:
                pxc.pxc_status = "failed"
                update_polardbx_record(pxc, ex)
                raise ex

        return wrapper

    return decorator

def update_polardbx_record(pxc, ex=None):
    try:
        sql = f"replace into polardbx_cluster ('id', 'gmt_created', 'gmt_modified', 'pxc_name', 'pxc_status', 'cn_replica', " \
              f"'cn_version', 'dn_replica', 'dn_version', 'leader_only', 'root_account', 'root_password', 'details', " \
              f"'cdc_replica', 'cdc_version') values (" \
              f"NULL, date('now'), date('now'), '{pxc.pxc_name}', '{pxc.pxc_status}', '{pxc.cn_replica}', '{pxc.cn_version}', " \
              f"'{pxc.dn_replica}', '{pxc.dn_version}', '{pxc.leader_only}', '{pxc.root_account}', '{pxc.root_password}', " \
              f"'{str(ex)}', '{pxc.cdc_replica}', '{pxc.cdc_version}')"
        SQLiteManager.execute_update(sql)
    except Exception as ex:
        logger.error("failed to update polardbx record", ex)


def xdb_create_task(task_name="DEFAULT"):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            xdb = args[0]
            try:
                logger.info('task_name: %s, call %s():', task_name, func.__name__)
                ret = func(*args, **kw)
                update_xdb_record(xdb)
                return ret
            except Exception as ex:
                xdb.status = 'fail'
                update_xdb_record(xdb, ex)
                raise ex

        return wrapper

    return decorator

def update_xdb_record(xdb, ex=None):
    try:
        sql = f"replace into polardbx_xdb ('id', 'gmt_created', 'gmt_modified', 'xdb_name', 'xdb_status', 'xdb_type'," \
              f" 'pxc_name', 'version', 'leader_only', 'leader_container_name', 'root_account', 'root_password', 'details') " \
              f"values (NULL, date('now'), date('now'), '{xdb.name}', '{xdb.status}', '{xdb.xdb_type}'" \
              f", '{xdb.pxc_name}', '{xdb.version}', '{xdb.leader_only}', " \
              f"'{xdb.leader_node.name if xdb.leader_node != None else None}','{xdb.user_name}', '{xdb.password}', " \
              f"'{str(ex)}')"
        SQLiteManager.execute_update(sql)
    except Exception as ex:
        logger.error("failed to update polardbx record", ex)