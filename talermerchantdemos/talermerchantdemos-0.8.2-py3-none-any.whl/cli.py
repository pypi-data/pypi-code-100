##
# This file is part of GNU Taler
# (C) 2017,2021 Taler Systems S.A.
#
# GNU Taler is free software; you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation; either
# version 3, or (at your option) any later version.
#
# GNU Taler is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public
# License along with GNU Taler; see the file COPYING.  If not,
# see <http://www.gnu.org/licenses/>
#
#  @author Florian Dold
#  @file Standalone script to run the blog.

import click
import logging
import argparse
import sys
import os
import site
from taler.util.talerconfig import TalerConfig, ConfigurationError

LOGGER = logging.getLogger(__name__)
# No perfect match to our logging format, but good enough ...
UWSGI_LOGFMT = "%(ltime) %(proto) %(method) %(uri) %(proto) => %(status)"

# Argument to tell uWSGI to load the python plugin.
# This hack is required, because on systems where the plugin is statically linked,
# loading it causes an error.
arg_load_python = "--if-not-plugin python --plugins python --endif".split(" ")

##
# This function interprets the 'serve-uwsgi' subcommand.
# The effect is to launch the blog UWSGI service.  This
# type of service is usually used when the HTTP blog interface
# is accessed via a reverse proxy (like Nginx, for example).
#
# @param command line options.
def handle_serve_uwsgi(config, which_shop):
    serve_uwsgi = config[which_shop]["uwsgi_serve"].value_string(required=True).lower()
    params = [
        "uwsgi",
        "uwsgi",
        *arg_load_python,
        "--master",
        "--die-on-term",
        "--log-format",
        UWSGI_LOGFMT,
        "--module",
        "talermerchantdemos.{}:app".format(which_shop),
        "--need-app",
        "--cache2",
        "name=paid_articles,items=500",
    ]
    if serve_uwsgi == "tcp":
        port = config[which_shop]["uwsgi_port"].value_int(required=True)
        spec = ":%d" % (port,)
        params.extend(["--socket", spec])
    elif serve_uwsgi == "unix":
        spec = config[which_shop]["uwsgi_unixpath"].value_filename(required=True)
        mode = config[which_shop]["uwsgi_unixpath_mode"].value_filename(required=True)
        params.extend(["--socket", spec])
        params.extend(["--chmod-socket=" + mode])
        os.makedirs(os.path.dirname(spec), exist_ok=True)
    logging.info("launching uwsgi with argv %s", params[1:])
    try:
        os.execlp(*params)
    except:
        sys.stderr.write(
            "Failed to start uwsgi. Please make sure to install uwsgi for Python3."
        )
        sys.exit(1)


##
# This function interprets the 'serve-http' subcommand.
# The effect it to launch the blog HTTP service.
#
# @param args command line options.
def handle_serve_http(config, which_shop, port=None):
    if port is None:
        port = config[which_shop]["http_port"].value_int(required=True)
    if port is None:
        print("'http_port' configuration option is missing")
        exit(1)
    spec = ":%d" % (port,)
    try:
        os.execlp(
            "uwsgi",
            "uwsgi",
            *arg_load_python,
            "--master",
            "--die-on-term",
            "--log-format",
            UWSGI_LOGFMT,
            "--http",
            spec,
            "--module",
            "talermerchantdemos.{}:app".format(which_shop),
        )
    except:
        sys.stderr.write(
            "Failed to start uwsgi. Please make sure to install uwsgi for Python3."
        )
        sys.exit(1)


def handle_serve_from_config(config_obj, which_shop):
    try:
        if (
            config_obj.value_string(which_shop, "serve", required=True).lower()
            == "http"
        ):
            return handle_serve_http(config_obj, which_shop)
        handle_serve_uwsgi(config_obj, which_shop)
    except ConfigurationError as ce:
        print(ce)
        exit(1)


@click.command("Global shop launcher")
@click.option("-c", "--config", help="Configuration file", required=False)
@click.option(
    "--http-port",
    help="HTTP port to serve (if not given, serving comes from config)",
    required=False,
    type=int,
)
@click.argument("which-shop")
def demos(config, http_port, which_shop):
    """WHICH_SHOP is one of: blog, donations, survey or landing."""

    if which_shop not in ["blog", "donations", "landing", "survey"]:
        print("Please use a valid shop name: blog, donations, landing, survey.")
        sys.exit(1)
    config_obj = TalerConfig.from_file(config)
    if http_port:
        return handle_serve_http(config_obj, which_shop, http_port)
    handle_serve_from_config(config_obj, which_shop)


demos()
