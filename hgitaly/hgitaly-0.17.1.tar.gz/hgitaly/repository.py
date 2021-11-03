# Copyright 2021 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later

GITLAB_PROJECT_FULL_PATH_FILENAME = b'gitlab.project_full_path'


def set_gitlab_project_full_path(repo, full_path: bytes):
    """Store information about the full path of GitLab Project.

    In GitLab terminology, ``full_path`` is the URI path, while ``path``
    its the last segment of ``full_path``.

    In Git repositories, this is stored in config. We could as well use
    the repo-local hgrcs, but it is simpler to use a dedicated file, and
    it makes sense to consider it not part of ``store`` (``svfs``), same
    as ``hgrc``.
    """
    with repo.wlock():
        repo.vfs.write(GITLAB_PROJECT_FULL_PATH_FILENAME, full_path)
