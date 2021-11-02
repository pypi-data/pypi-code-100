from __future__ import annotations

from functools import cached_property


class Ref(str):
    @cached_property
    def uri(self):
        uri, *_ = self.partition("#")
        if uri:
            return uri

    @cached_property
    def anchor(self):
        *_, fragment = self.partition("#")
        if fragment and not fragment.startswith("/"):
            return fragment

    @cached_property
    def pointer(self):
        *_, fragment = self.partition("#")
        if fragment and fragment.startswith("/"):
            return fragment

    @cached_property
    def decomposed(self):
        return (self.uri, self.pointer, self.anchor)


def push_fragments(a: str, *fragments: str | int):
    output = a
    for fragment in fragments:
        output = output + "/" + str(fragment)
    return output


def push_pointer(a: str, *fragments: str | int):
    output = a or ""
    if "#" not in output:
        output = output + "#"
    for fragment in fragments:
        output = output + "/" + str(fragment)
    return output
