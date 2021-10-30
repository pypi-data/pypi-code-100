from typing import List
from git_conventional_version.versioning.versions import Version
from git import Repo
from git.exc import GitCommandError
import re


class Conventional:
    """Handles incrementing versions based on commit messages.
    """
    major_patterns = [r"breaking change:"]
    minor_patterns = [r"^feat(\(.*\))?:"]
    patch_patterns = [r"^fix(\(.*\))?:"]

    def __init__(
        self,
        repo: Repo
    ) -> None:
        self.repo = repo

    def increment(self, version: Version) -> Version:
        if self._check_for(version, self.major_patterns):
            version.numbers[0] += 1
            version.numbers[1] = 0
            version.numbers[2] = 0
        elif self._check_for(version, self.minor_patterns):
            version.numbers[1] += 1
            version.numbers[2] = 0
        elif self._check_for(version, self.patch_patterns):
            version.numbers[2] += 1
        return version

    def _check_for(self, version: Version, patterns: List[str]) -> bool:
        messages = self._get_messages(version)
        for pattern in patterns:
            for message in messages:
                if re.search(pattern, message, re.IGNORECASE):
                    return True
        return False

    def _get_messages(self, version: Version) -> List[str]:
        """Get commit messages that are needed to check for increment.

        That means get commits since last final version and
        if it is only on different branch, get commits on current
        branch that are not present on the other branch since that
        final version commit.

        Args:
            version: version to check bump for.

        Returns:
            List of commit messages.
        """
        messages = []
        version_string = str(version)
        active_branch =self.repo.active_branch
        if version_string in self.repo.references:
            commits = self.repo.iter_commits(
                rev=f"{version_string}..{active_branch}"
            )
        else:
            commits = self.repo.iter_commits(
                rev=f"{active_branch}"
            )
        while True:
            try:
                try:
                    commit = next(commits)
                except GitCommandError:
                    break
                messages.append(commit.message)
            except StopIteration:
                break
        return messages
