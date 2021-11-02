#
#  The OpenDiamond Platform for Interactive Search
#
# SPDX-License-Identifier: EPL-1.0
#
#  Copyright (c) 2021 Carnegie Mellon University
#  All rights reserved.
#
#  This software is distributed under the terms of the Eclipse Public
#  License, Version 1.0 which can be found in LICENSES/EPL-1.0.
#  ANY USE, REPRODUCTION OR DISTRIBUTION OF THIS SOFTWARE CONSTITUTES
#  RECIPIENT'S ACCEPTANCE OF THIS AGREEMENT
#
"""Functions to assist with handling application/x-diamond-scope files"""

import click

from .scope_generate import generate
from .scope_import import import_, install, uninstall
from .scope_options import CONTEXT_SETTINGS
from .scope_verify import verify


@click.group("scope", context_settings=CONTEXT_SETTINGS)
def cli():
    """Scope handling related functions"""


cli.add_command(generate)
cli.add_command(import_)
cli.add_command(install)
cli.add_command(uninstall)
cli.add_command(verify)
