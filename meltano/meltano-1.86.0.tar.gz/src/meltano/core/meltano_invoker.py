"""Defines MeltanoInvoker."""
import os
import subprocess
import sys
from pathlib import Path

from .project import Project
from .project_settings_service import ProjectSettingsService, SettingValueStore

MELTANO_COMMAND = "meltano"


class MeltanoInvoker:
    def __init__(self, project, settings_service: ProjectSettingsService = None):
        self.project = project
        self.settings_service = settings_service or ProjectSettingsService(project)

    def invoke(self, args, command=MELTANO_COMMAND, env=None, **kwargs):
        """Invoke `meltano` (or provided command) with provided args and env."""
        return subprocess.run(
            [self._executable_path(command), *args],
            **kwargs,
            env=self._executable_env(env)
        )

    def _executable_path(self, command):
        if command == MELTANO_COMMAND:
            # This symlink is created by Project.activate
            executable_symlink = self.project.run_dir().joinpath("bin")
            if executable_symlink.exists():
                return str(executable_symlink)

        executable = Path(os.path.dirname(sys.executable), command)
        if executable.exists():
            return str(executable)

        # Fall back on expecting command to be in the PATH
        return command

    def _executable_env(self, env=None):
        exec_env = {}

        # Include env that project settings are evaluated in
        exec_env.update(self.settings_service.env)

        # Include env for settings explicitly overridden using CLI flags
        exec_env.update(
            self.settings_service.as_env(source=SettingValueStore.CONFIG_OVERRIDE)
        )

        # Include explicitly provided env
        if env:
            exec_env.update(env)

        return exec_env
