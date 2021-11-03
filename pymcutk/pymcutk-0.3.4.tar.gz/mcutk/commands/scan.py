#
# MIT License
# 
# Copyright 2021 NXP
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import os
import json
import yaml
import click

from mcutk.projects_scanner import find_projects


@click.command('scan', short_help='projects scanner')
@click.argument('path', required=True, type=click.Path(exists=True))
@click.option('-o', '--output', type=click.Path(exists=False), help='dump scan results to file, file format support: json or yml.')
@click.option('--dapeng', is_flag=True, default=False, hidden=True, help='dump for dapeng style, casfile.yml')
def cli(path, output, dapeng):
    """Scan projects from specificed directory and dump to file(json or yml)."""

    projects, count = find_projects(path, True)
    dataset = list()

    if output:
        extension = os.path.basename(output).split(".")[-1]
        for tname, plist in projects.items():
            for project in plist:
                dataset.append(project.to_dict())

        if extension in ('yml', 'yaml'):
            with open(output, 'w') as file:
                yaml.safe_dump(dataset, file, default_flow_style=False)
        else:
            with open(output, 'w') as file:
                json.dump(dataset, file)

        # elif format == 'dapeng':
        #     for project in projects:
        #         if project.path
        # else:
        #     pass

        click.echo("output file: %s" % output)
