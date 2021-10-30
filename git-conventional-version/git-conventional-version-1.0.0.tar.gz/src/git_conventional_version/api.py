from git_conventional_version.changelog.changelog import Changelog
from git_conventional_version.versioning.conventional import Conventional
from git_conventional_version.versioning.releases import \
    AlphaRelease, \
    BetaRelease, \
    DevelopmentalRelease, \
    FinalRelease, \
    Release, \
    ReleaseCandidateRelease
from git import Repo


version_types = ["final", "rc", "dev", "beta", "alpha", "local"]


class InvalidVersionTypeError(Exception):
    pass


class Api:
    """Provides interface for main functionalities.
    """
    def __init__(
        self,
        repo: Repo
    ) -> None:
        self.repo = repo

    def _create_release(self, type: str="final") -> Release:
        if type == "final":
            release = FinalRelease(self.repo)
        elif type == "rc":
            release = ReleaseCandidateRelease(self.repo)
        elif type == "dev":
            release = DevelopmentalRelease(self.repo)
        elif type == "beta":
            release = BetaRelease(self.repo)
        elif type == "alpha":
            release = AlphaRelease(self.repo)
        else:
            raise Exception(f"Type: '{type}' is not valid.")
        return release

    def get_old_version(self, type: str) -> str:
        return str(self._create_release(type).get_old_version())

    def get_new_version(self, type: str) -> str:
        return str(self._create_release(type).get_new_version())

    def get_local_version(self) -> str:
        return str(self._create_release().get_local_version())

    def get_changelog(self) -> str:
        return Changelog(
            repo=self.repo,
            release=self._create_release(),
            header_patterns=
                Conventional.major_patterns + 
                Conventional.minor_patterns + 
                Conventional.patch_patterns
        ).generate()
