from typing import List
from git.refs.tag import Tag
from git import Repo
from git_conventional_version.versioning.conventional import Conventional 
from git_conventional_version.versioning.versions import \
    AlphaVersion, \
    BetaVersion, \
    DevelopmentalVersion, \
    FinalVersion, \
    ReleaseCandidateVersion, \
    Version
import re


class Release:
    """Handles specific type of version.

    Release implementations should have version_class defined.
    Each Release has corresponding Version class defined.
    """
    version_class = Version

    def __init__(
        self,
        repo: Repo
    ) -> None:
        self.repo = repo 
        self.conventional = Conventional(self.repo)

    def get_old_version(self) -> Version:
        version_strings = self._get_version_strings()
        version_strings = self._sort_version_strings(version_strings)
        if len(version_strings) > 0:
            return self.version_class.from_tag(version_strings[0])
        else:
            return self.version_class()

    def get_new_version(self) -> Version:
        return self.conventional.increment(self.get_old_version())

    def get_version_tags(self) -> List[Tag]:
        return [tag for tag in self.repo.tags if re.search(self.version_class.pattern, str(tag))]

    def _get_version_strings(self) -> List[str]:
        return [str(vt) for vt in self.get_version_tags()]

    def _sort_version_strings(self, version_strings: List[str]) -> List[str]:
        return sorted(
            version_strings,
            key=lambda x: tuple(re.findall(r'\d+', x)),
            reverse=True
        )


class FinalRelease(Release):
    """Handles final versions.
    """
    version_class = FinalVersion


class PreRelease(Release):
    """Handles general pre-release versions like rc or dev.

    Needs subclassing.
    """
    def __init__(
        self,
        repo: Repo
    ) -> None:
        super().__init__(repo)
        self.final_release = FinalRelease(repo)
        
    def get_old_version(self) -> Version:
        pre_release_version = super().get_old_version()
        final_version = self.final_release.get_new_version()
        if pre_release_version.numbers[3] == 0 \
        or final_version.numbers != pre_release_version.numbers[:3]:
            pre_release_version = self.version_class(
                numbers=final_version.numbers + [0]
            )
        return pre_release_version

    def get_new_version(self) -> Version:
        pre_release_version = self.get_old_version()
        try:
            if self.repo.head.commit.hexsha \
            == self.repo.tag(str(pre_release_version)).commit.hexsha:
                return pre_release_version
        except ValueError:
            pass
        pre_release_version.numbers[3] += 1
        return pre_release_version


class ReleaseCandidateRelease(PreRelease):
    """Handles pre-release versions specifically.
    """
    version_class = ReleaseCandidateVersion


class DevelopmentalRelease(PreRelease):
    """Handles developmental versions specifically.
    """
    version_class = DevelopmentalVersion


class AlphaRelease(PreRelease):
    """Handles beta versions specifically.
    """
    version_class = AlphaVersion


class BetaRelease(PreRelease):
    """Handles beta versions specifically.
    """
    version_class = BetaVersion