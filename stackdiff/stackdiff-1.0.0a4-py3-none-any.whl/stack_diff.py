from functools import cached_property
from typing import IO, Optional

from ansiscape import green, heavy, yellow
from boto3.session import Session
from differently import render
from tabulate import tabulate


class StackDiff:
    """
    Visualises the changes described by an Amazon Web Services CloudFormation
    change set.

    Arguments:
        change:  ARN, ID or name of the CloudFormation change set to visualise
        session: boto3 session (defaults to a new session)
        stack:   ARN, ID or name of the change set's CloudFormation stack
    """

    def __init__(
        self,
        change: str,
        stack: str,
        session: Optional[Session] = None,
    ) -> None:
        session = session or Session()

        self.change = change
        self.client = session.client(
            "cloudformation"
        )  # pyright: reportUnknownMemberType=false
        self.stack = stack

    def _make_action(self, action: str, replacement: str) -> str:
        if action != "Modify":
            return action

        rl = replacement.lower()

        if rl == "true":
            return "Replace 🔥"

        if rl == "false":
            return "Update"

        return "Conditionally 🔥"

    @cached_property
    def change_template(self) -> str:
        """Gets the change set's proposed template."""

        response = self.client.get_template(
            ChangeSetName=self.change,
            StackName=self.stack,
            TemplateStage="Original",
        )
        return response.get("TemplateBody", "")

    def render_changes(self, writer: IO[str]) -> None:
        """
        Renders a visualisation of the changes that CloudFormation would apply
        if the change set was executed.

        Arguments:
            writer: Writer
        """

        response = self.client.describe_change_set(
            ChangeSetName=self.change,
            StackName=self.stack,
        )

        rows = [
            [
                heavy("Logical ID").encoded,
                heavy("Physical ID").encoded,
                heavy("Resource Type").encoded,
                heavy("Action").encoded,
            ]
        ]

        for change in response["Changes"]:
            rc = change.get("ResourceChange", None)
            if not rc:
                continue

            if rc["Action"] == "Add":
                color = green
            else:
                color = yellow

            action = self._make_action(
                action=rc["Action"],
                replacement=rc.get("Replacement", "False"),
            )

            # PhysicalResourceId is not present for additions:
            physical_id = rc.get("PhysicalResourceId", "")
            fmt_physical_id = color(physical_id).encoded if physical_id else ""

            rows.append(
                [
                    color(rc["LogicalResourceId"]).encoded,
                    fmt_physical_id,
                    color(rc["ResourceType"]).encoded,
                    color(action).encoded,
                ]
            )

        t = tabulate(rows, headers="firstrow", tablefmt="plain")
        writer.write(t + "\n")

    def render_differences(self, writer: IO[str]) -> None:
        """
        Renders a visualisation of the differences between the stack's current
        template and the change set's proposed template.

        Arguments:
            writer: Writer
        """

        render(self.stack_template, self.change_template, writer)

    @cached_property
    def stack_template(self) -> str:
        """Gets the stack's current template."""

        response = self.client.get_template(
            StackName=self.stack,
            TemplateStage="Original",
        )
        return response.get("TemplateBody", "")
