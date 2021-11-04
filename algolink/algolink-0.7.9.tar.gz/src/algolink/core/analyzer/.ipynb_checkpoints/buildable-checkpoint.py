from abc import ABC

from algolink.core.analyzer import Hook, analyzer_class
from algolink.core.objects.core import Buildable


class BuildableHook(Hook, ABC):
    pass


BuildableAnalyzer = analyzer_class(BuildableHook, Buildable)
