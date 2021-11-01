"""
JSON schema loader helpers
"""

from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


class MergeStrategy(ABC):
    """A base class to represent a schema merge strategy."""

    base: Dict[str, Any]
    to_merge: Dict[str, Any]

    @abstractmethod
    def merge(self) -> Dict[str, Any]:
        """Perform the merge operation."""


@dataclass
class MergeBase:
    base: Dict[str, Any] = field(default_factory=dict)
    to_merge: Dict[str, Any] = field(default_factory=dict)


@dataclass
class KeyStore:
    to_pop: List[str] = field(default_factory=list)

    def pop_key(self, key: str) -> None:
        self.to_pop.append(key)


@dataclass
class AndMergeStrategy(MergeStrategy, MergeBase, KeyStore):
    neg: bool = False

    def remove_item_from_list(self, val: List[Any], item: Any) -> None:
        try:
            val.remove(item)
        except ValueError:
            pass

    def handle_sub_merge(
        self, base: Dict[str, Any], to_merge: Dict[str, Any], neg: Optional[bool] = None
    ) -> None:
        if neg is None:
            neg = self.neg
        merger = AndMergeStrategy(
            base=base,
            to_merge=to_merge,
            neg=neg
        )
        merger.merge()

    def handle_dict(self, key: str, val: Dict[str, Any]) -> None:
        to_merge_val = self.to_merge.get(key)
        if to_merge_val is None:
            return
        if self.neg and to_merge_val == val:
            self.pop_key(key)
        else:
            self.handle_sub_merge(val, to_merge_val, self.neg)

    def handle_enum(self, key: str, val: Any) -> None:
        to_merge_val = self.to_merge.get(key)
        if to_merge_val is None:
            return
        if self.neg:
            s = set(val).intersection(to_merge_val)
        else:
            s = set(val).symmetric_difference(to_merge_val)
        for v in s:
            self.remove_item_from_list(val, v)

    def handle_required(self, key: str, val: Any) -> None:
        to_merge_val = self.to_merge.get(key)
        if to_merge_val is None:
            return
        for v in to_merge_val:
            if self.neg:
                self.remove_item_from_list(val, v)
            else:
                if v not in val:
                    val.append(v)

    def handle_list(self, key: str, val: List[Any]) -> None:
        to_merge_val = self.to_merge.get(key)
        if to_merge_val is None:
            self.base[key] = val
            return
        if not isinstance(to_merge_val, list):
            raise KeyError
        if key == "enum":
            self.handle_enum(key, val)
        elif key == "required":
            self.handle_required(key, val)

    def handle_base_default(self, key: str, val: Any) -> None:
        to_merge_val = self.to_merge.get(key)
        if to_merge_val is None:
            return
        if self.neg and key not in ["type", "description"]:
            self.base[key] = {"not": to_merge_val}
        elif key != "$ref":
            self.base[key] = to_merge_val

    def handle_base_item(self, key: str, val: Any) -> None:
        if key in ["$or", "$xor"]:
            return
        elif key == "not":
            self.handle_sub_merge(self.to_merge, val, True)
        elif isinstance(val, dict):
            self.handle_dict(key, val)
        elif isinstance(val, list):
            self.handle_list(key, val)
        else:
            self.handle_base_default(key, val)

    def handle_base_keys(self) -> None:
        for key, val in self.base.items():
            self.handle_base_item(key, val)

    def handle_to_merge_default(self, key: str) -> None:
        if self.neg and key not in ["type", "description"]:
            self.base[key] = {"not": self.to_merge[key]}
        elif key == "$ref":
            if key not in self.base.keys():
                self.base[key] = self.to_merge[key]
        else:
            self.base[key] = self.to_merge[key]

    def handle_to_merge_or(self, key: str) -> None:
        base_val = self.base.get(key)
        if base_val is None:
            self.base[key] = [{}]
            return
        for v in self.to_merge.pop(key):
            if v:
                base_val.append(v)

    def handle_to_merge_item(self, key: str) -> None:
        if key in ["$or", "$xor"]:
            self.handle_to_merge_or(key)
        elif key == "not":
            self.handle_sub_merge(self.base, self.to_merge[key], True)
        else:
            self.handle_to_merge_default(key)

    def handle_to_merge_keys(self) -> None:
        base_keys = self.base.keys()
        to_merge_keys = self.to_merge.keys()
        unique_to_merge_keys = set(to_merge_keys).difference(base_keys)
        for key in unique_to_merge_keys:
            self.handle_to_merge_item(key)

    def handle_keys_to_pop(self):
        for key in self.to_pop:
            self.base.pop(key)

    def merge(self) -> Dict[str, Any]:
        if not self.base:
            self.base.update(self.to_merge)
            return self.base
        self.handle_base_keys()
        self.handle_to_merge_keys()
        self.handle_keys_to_pop()
        return self.base


@dataclass
class OrMergeStrategy(MergeStrategy, MergeBase, KeyStore):
    """Merge json schemas assuming a 'oneOf' or 'anyOf' command

    The idea is to find out the differences between 'base' and 'to_merge'. If a
    property is in 'base' and not in 'to_merge', it is added to all the
    alternative properties except 'to_merge'. If a property is in 'base' and in
    'to_merge', it's removed from 'to_merge' and 'base' is left as is
    """

    exclusive: bool = False

    @property
    def operand(self) -> str:
        return "$%sor" % ("x" if self.exclusive else "")

    def handle_base_only_key(self, key: str) -> None:
        base_val = self.base[self.operand]
        if key.startswith("$"):
            return
        val = self.base.pop(key)
        for a in base_val:
            a[key] = val

    def handle_base_only_keys(self) -> None:
        base_val = self.base[self.operand]
        for key in set(self.base.keys()).difference(self.to_merge.keys()):
            self.handle_base_only_key(key)

    def handle_properties(self, key: str) -> None:
        prop_base = self.base.get(key, {})
        prop_mrg = self.to_merge[key]
        for p in set(prop_mrg.keys()).intersection(prop_base.keys()):
            prop_mrg.pop(p)

    def handle_required(self, key: str) -> None:
        req_mrg = self.to_merge[key]
        for p in set(req_mrg).intersection(self.base.get(key, [])):
            req_mrg.remove(p)

    def handle_default(self, key: str) -> None:
        if self.to_merge[key] == self.base.get(key, None):
            self.to_merge.pop(key)

    def handle_to_merge_only_key(self, key: str) -> None:
        if key.startswith("$"):
            return
        if key == "properties":
            self.handle_properties(key)
        elif key == "required":
            self.handle_required(key)
        else:
            self.handle_default(key)

    def handle_to_merge_only_keys(self) -> None:
        for key in set(self.to_merge.keys()).intersection(self.base.keys()):
            self.handle_to_merge_only_key(key)

    def merge(self) -> Dict[str, Any]:
        if not self.base:
            self.base.update(self.to_merge)
            self.base[self.operand] = [{}]
            return self.base
        if self.base.get(self.operand) is None:
            self.base[self.operand] = [{}]
        self.handle_base_only_keys()
        self.handle_to_merge_only_keys()
        base_val = self.base[self.operand]
        base_val.append(self.to_merge)
        return self.base


def merge(base: Dict[str, Any], to_merge: Dict[str, Any], mode: str) -> Dict[str, Any]:
    if mode in ["allOf", "allOfNot"]:
        merger = AndMergeStrategy(
            base=base,
            to_merge=to_merge,
            neg=(mode == "allOfNot")
        )
        return merger.merge()
    if mode in ["oneOf", "anyOf"]:
        merger = OrMergeStrategy(
            base=base,
            to_merge=to_merge,
            exclusive=(mode == "oneOf")
        )
        return merger.merge()
    raise RuntimeError('Merging mode "%s" is not supported yet' % mode)
