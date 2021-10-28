import re

from commitizen.cz.conventional_commits import ConventionalCommitsCz
from git.objects.commit import Commit
__version__ = "0.1.2"

class ConventionalJiraCommits(ConventionalCommitsCz):
    changelog_pattern = r"^(\[[A-Z]+\-[0-9]+\]) - (BREAKING[\-\ ]CHANGE|feat|fix|refactor|perf)(\(.+\))?(!)?"
    commit_parser = r"^(?P<issue>\[[A-Z]+\-[0-9]+\]) - (?P<change_type>feat|fix|refactor|perf|BREAKING CHANGE)(?:\((?P<scope>[^()\r\n]*)\)|\()?(?P<breaking>!)?:\s(?P<message>.*)?"  # noqa

    def questions(self) -> list:
        """Questions regarding the commit message."""
        questions = [
            {
                "type": "input",
                "name": "issue",
                "message": "Task/Feature do Jira",
            },
            *super().questions(),
        ]
        return questions

    def message(self, answers: dict) -> str:
        """Generate the message with the given answers."""
        return "[{}] - {}".format(
            answers.pop("issue"), super().message(answers)
        )

    def example(self) -> str:
        """Provide an example to help understand the style (OPTIONAL)

        Used by `cz example`.
        """
        return "[TSSU-001] - fix(src/settings.py): corrigido typos no código"

    def schema(self) -> str:
        """Show the schema used (OPTIONAL)

        Used by `cz schema`.
        """
        return "[<issue>] <type>(<scope>): <subject>"

    def info(self) -> str:
        """Explanation of the commit rules. (OPTIONAL)

        Used by `cz info`.
        """
        return "Usado para padronizar commits"

    def schema_pattern(self) -> str:
        return "".join((r"(\[[A-Z]+\-[0-9]+\])", super().schema_pattern()))

    def _process_commit(self, commit: str) -> str:
        pat = re.compile(self.schema_pattern())
        m = re.match(pat, commit)
        if m is None:
            return ""
        return " - ".join((m.group(1).strip(), m.group(4).strip()))

    def changelog_message_builder_hook(
        self, parsed_message: dict, commit: Commit
    ) -> dict:
        m = parsed_message["message"]
        issue = parsed_message["issue"].replace("[", "").replace("]", "")
        parsed_message[
            "message"
        ] = f"[{issue}](https://serasaexperian.atlassian.net/browse/{issue}) {m} [{commit.author}]({commit.author_email})"
        return parsed_message


discover_this = IpaasCz  # used by the plug-in system
