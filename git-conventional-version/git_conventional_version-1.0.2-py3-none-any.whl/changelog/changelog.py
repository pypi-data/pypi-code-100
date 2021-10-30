import re
from typing import Dict
from git.exc import GitCommandError


class Changelog():
    def __init__(
        self,
        repo,
        release,
        header_patterns
    ) -> None:
        self.repo = repo
        self.release = release
        self.header_patterns = header_patterns
    
    def _create_version_to_headers(self) -> Dict[str, list]:
        new_version = str(self.release.get_new_version())
        sha_to_version = { x.commit.hexsha:str(x) for x in self.release.get_version_tags()}
        commits = self.repo.iter_commits(rev=self.repo.active_branch)
        version_to_headers = {new_version: []}
        current_version = new_version
        while True:
            try:
                try:
                    commit = next(commits)
                except GitCommandError:
                    break
            except StopIteration:
                break 
            if commit.hexsha in sha_to_version:
                current_version = sha_to_version[commit.hexsha]
                if current_version not in version_to_headers:
                    version_to_headers[current_version] = []
            for line in commit.message.split("\n"):
                for pattern in self.header_patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        version_to_headers[current_version].append(line)
        return version_to_headers
    
    def _format(self, version_to_headers: Dict[str, list]) -> str:
        changelog = ""
        changelog += "# CHANGELOG\n"
        changelog += "\n"
        for k,v in version_to_headers.items():
            if v:
                changelog += f"## {k}\n"
                changelog += "\n"
            v = sorted(v)
            for i in v:
                changelog += f"- {i}\n"
            changelog += "\n"
        return changelog[:-1]
        
    def generate(self) -> str:
        version_to_headers = self._create_version_to_headers()
        return self._format(version_to_headers)
