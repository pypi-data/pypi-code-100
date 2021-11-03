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

from mcutk.exceptions import ToolchainError
from mcutk.apps import appfactory



def build_project(tool_name, tool_path, project_path, tool_version=None,
    target=None, logfile=None, workspace=None, timeout=300):
    """A simple shortcut method to build C/C++ projects for embedded toolchains.

    Arguments:
        tool_name {string} -- toolchain name, like: iar, mdk, mcux, armgcc...
        tool_path {string} -- toolchain installation root directory
        project_path {string} -- project root directory or project path
        workspace {string} -- workspace directory for Eclipse based toolchains
        timeout {int} -- timeout for build
        tool_version {string} -- set toolchain version
        target {string} -- project configuration, debug/release
        logfile {string} -- log file path (default: {None})

    Raises:
        ToolchainError -- raise on unsupported toolchain
        IOError -- raise on toolchain is not ready

    Returns:
        mcutk.apps.BuildResult -- build result
    """

    tool = appfactory(tool_name)
    if not tool:
        raise ToolchainError('unsupported tool: %s'%tool_name)

    toolchain = tool(tool_path, version=tool_version)
    if not toolchain.is_ready:
        raise IOError('tool is not ready to use, path: %s!' % tool_path)

    project = tool.Project.frompath(project_path)

    if target:
        target = project.map_target(target)
    else:
        target = project.targets[0]

    ret = toolchain.build_project(project, target, logfile, workspace=workspace, timeout=timeout)

    return ret
