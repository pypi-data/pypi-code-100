from typing import Any, Mapping, Sequence


class StringSequenceExtractor(object):
    def extract(self, instance: Mapping[str, Any]) -> Sequence[str]:
        raise NotImplementedError()
