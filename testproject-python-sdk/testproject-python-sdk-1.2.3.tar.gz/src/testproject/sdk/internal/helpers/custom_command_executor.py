# Copyright 2020 TestProject (https://testproject.io)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from selenium.webdriver.remote.remote_connection import RemoteConnection

from src.testproject.sdk.internal.agent import AgentClient
from src.testproject.sdk.internal.helpers.reporting_command_executor import ReportingCommandExecutor


class CustomCommandExecutor(RemoteConnection, ReportingCommandExecutor):
    """Extension of the Selenium RemoteConnection (command_executor) class

    Args:
        agent_client (AgentClient): Client used to communicate with the TestProject Agent
        remote_server_addr (str): Remote server (Agent) address
    """

    def __init__(self, agent_client: AgentClient, remote_server_addr: str):
        RemoteConnection.__init__(self, remote_server_addr=remote_server_addr)
        ReportingCommandExecutor.__init__(
            self,
            agent_client=agent_client,
            command_executor=self,
            remote_connection=super(),
        )
        self.w3c = self.step_helper.w3c  # Selenium expects the w3c as a class member

    def execute(self, command: str, params: dict, skip_reporting: bool = False):
        """Execute a Selenium command

        Args:
            command (str): A string specifying the command to execute
            params (dict): A dictionary of named parameters to send with the command as its JSON payload
            skip_reporting (bool): True if command should not be reported to Agent, False otherwise

        Returns:
            response: Response returned by the Selenium remote WebDriver server
        """
        self.update_known_test_name()

        self.step_helper.handle_timeout(self.settings.timeout)

        # Handling sleep before execution
        self.step_helper.handle_sleep(self.settings.sleep_timing_type, self.settings.sleep_time, command)

        response = super().execute(command=command, params=params)

        # Handling sleep after execution
        self.step_helper.handle_sleep(self.settings.sleep_timing_type, self.settings.sleep_time, command, True)

        result = response.get("value")

        passed = self.is_command_passed(response=response)

        if not skip_reporting:
            self._report_command(command, params, result, passed)

        return response
