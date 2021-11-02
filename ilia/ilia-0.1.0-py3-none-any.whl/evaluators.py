from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from decimal import Decimal
from functools import reduce
from types import NotImplementedType
from typing import (
    Any,
    Callable,
    Generic,
    Iterable,
    Iterator,
    Protocol,
    Type,
    TypeVar,
    cast,
    overload,
)

from .checkers import is_type
from .ref import push_fragments

T = TypeVar("T", covariant=True)
U = TypeVar("U")


class Keyword(Protocol):
    @property
    def relative_location(self) -> str:
        ...

    @property
    def absolute_keyword_location(self) -> str:
        ...


@dataclass
class Instance(Generic[T]):
    location: str
    value: T
    parent: Instance | None = None

    @overload
    def __iter__(self: Instance[dict]) -> Iterator[tuple[str, Instance]]:
        ...

    @overload
    def __iter__(self: Instance[list]) -> Iterator[tuple[int, Instance]]:
        ...

    def __iter__(self) -> Iterator[tuple[str | int, Instance]]:
        if isinstance(self.value, dict):
            iterable: Iterable[tuple[str | int, Any]] = self.value.items()
        elif isinstance(self.value, list):
            iterable = enumerate(self.value)
        else:
            raise AttributeError(f"Instance[{type(self.value)}] is not iterable")
        for name, member in iterable:
            yield name, Instance(
                location=push_fragments(self.location, name), value=member, parent=self
            )

    @property
    def names(self) -> InstanceContext[list[str]]:
        if isinstance(self.value, dict):
            names = list(self.value)
            return self.ctx(names)
        else:
            raise AttributeError(f"Instance[{type(self.value)}] is not iterable")

    def ctx(self, value: U) -> InstanceContext[U]:
        return InstanceContext(value=value, instance=self)


@dataclass
class InstanceContext(Generic[T]):
    value: T
    instance: Instance

    @property
    def location(self):
        return self.instance.location

    def __iter__(self) -> Iterator[InstanceContext]:
        if isinstance(self.value, list):
            for element in self.value:
                yield InstanceContext(value=element, instance=self.instance)


class Evaluable(Protocol[T]):
    @property
    def value(self) -> T:
        ...

    @property
    def location(self) -> str:
        ...


@dataclass
class Evaluation:
    valid: bool
    relative_location: str
    absolute_keyword_location: str
    instance: Instance
    value: Any = None
    reason: str | None = None
    evaluations: list[Evaluation] = field(default_factory=list)

    @property
    def instance_value(self):
        return self.instance.value

    @property
    def instance_location(self):
        return self.instance.location

    @property
    def keyword(self):
        return self.relative_location.rpartition("/")[-1]

    def __post_init__(self):
        if self.valid and self.reason is not None:
            raise Exception("reason is for errors")


class Evaluate(Protocol):
    def __call__(self, _0: Evaluable[T], /) -> Iterable[Evaluation]:
        raise NotImplementedError


def render(
    keyword: Keyword,
    subject: Instance | InstanceContext,
    valid: bool,
    value: Any = None,
    reason: str = None,
    evaluations: list[Evaluation] = None,
) -> Evaluation:
    if isinstance(subject, InstanceContext):
        instance = subject.instance
    else:
        instance = subject
    return Evaluation(
        valid=valid,
        value=value if valid else None,
        reason=reason if not valid else None,
        relative_location=keyword.relative_location,
        absolute_keyword_location=keyword.absolute_keyword_location,
        instance=instance,
        evaluations=evaluations or [],
    )


class AlwaysTrue:
    def __init__(self, relative_location: str, absolute_keyword_location: str):
        self.relative_location = relative_location
        self.absolute_keyword_location = absolute_keyword_location

    def __call__(self, instance: Instance, /) -> Iterable[Evaluation]:
        yield render(self, subject=instance, valid=True)


class AlwaysFalse:
    def __init__(self, relative_location: str, absolute_keyword_location: str):
        self.relative_location = relative_location
        self.absolute_keyword_location = absolute_keyword_location

    def __call__(self, instance: Instance, /) -> Iterable[Evaluation]:
        yield render(self, subject=instance, valid=False)

    def __repr__(self):
        return "AlwaysFalse()"


class Cluster:
    def __init__(
        self,
        evaluators: list[Evaluate],
        unevaluated_items: UnevaluatedItems,
        unevaluated_props: UnevaluatedProperties,
        relative_location: str,
        absolute_keyword_location: str,
    ):
        self.evaluators = evaluators
        self.unevaluated_items = unevaluated_items
        self.unevaluated_props = unevaluated_props
        self.relative_location = relative_location
        self.absolute_keyword_location = absolute_keyword_location

    def __call__(self, instance: Instance, /) -> Iterable[Evaluation]:
        evaluations: list[Evaluation] = []
        for evaluator in self.evaluators:
            evaluations += evaluator(instance)
        evaluations += self.yield_unevaluated_items(instance, evaluations)
        evaluations += self.yield_unevaluated_props(instance, evaluations)
        valid = not any(e.valid is False for e in evaluations)
        yield render(self, subject=instance, valid=valid, evaluations=evaluations)

    def __repr__(self):
        return f"Cluster(evaluators={self.evaluators!r}, unevaluated_items={self.unevaluated_items!r}, unevaluated_props={self.unevaluated_props!r})"

    def yield_unevaluated_items(
        self, instance: Instance, evaluations: list[Evaluation]
    ):
        if self.unevaluated_items and isinstance(instance.value, list):
            evaluated = get_evaluated_items(instance, evaluations)
            yield from self.unevaluated_items(instance, ignore=evaluated)

    def yield_unevaluated_props(
        self, instance: Instance, evaluations: list[Evaluation]
    ):
        if self.unevaluated_props and isinstance(instance.value, dict):
            evaluated = get_evaluated_props(instance, evaluations)
            yield from self.unevaluated_props(instance, ignore=evaluated)


def get_evaluated_items(
    instance: Instance[list], evaluations: list[Evaluation]
) -> set[int]:
    evaluated: set[int] = set()
    for evaluation in walk_annotations(instance, evaluations):
        if evaluation.keyword in (
            "prefixItems",
            "items",
            "contains",
            "unevaluatedItems",
        ):
            evaluated |= evaluation.value
    return evaluated


def get_evaluated_props(
    instance: Instance[dict], evaluations: list[Evaluation]
) -> set[str]:
    evaluated: set[str] = set()
    for evaluation in walk_annotations(instance, evaluations):
        if evaluation.keyword in (
            "properties",
            "patternProperties",
            "additionalProperties",
            "unevaluatedProperties",
        ):
            evaluated |= evaluation.value
    return evaluated


def walk_annotations(instance: Instance, evaluations: list[Evaluation]):
    queue = deque(evaluations)
    while queue:
        evaluation = queue.popleft()
        if evaluation.valid is False:
            continue
        if evaluation.evaluations:
            queue.extend(evaluation.evaluations)
        if evaluation.instance is instance and evaluation.value is not None:
            yield evaluation


class TypeValidator:
    def __init__(
        self,
        types: list[str],
        relative_location: str,
        absolute_keyword_location: str,
    ):
        self.types = types
        self.relative_location = relative_location
        self.absolute_keyword_location = absolute_keyword_location

    def __call__(self, instance: Instance) -> Iterable[Evaluation]:
        valid = is_type(instance.value, *self.types)
        yield render(self, valid=valid, subject=instance)

    def __repr__(self):
        return f"TypeValidator({self.types!r})"


class Not:
    def __init__(
        self,
        evaluator: Evaluate,
        relative_location: str,
        absolute_keyword_location: str,
    ):
        self.evaluator = evaluator
        self.relative_location = relative_location
        self.absolute_keyword_location = absolute_keyword_location

    def __call__(self, instance: Instance, /) -> Iterable[Evaluation]:
        evaluations: list[Evaluation] = []
        evaluations += self.evaluator(instance)
        valid = any(e.valid is False for e in evaluations)
        yield render(self, valid=valid, subject=instance, evaluations=evaluations)


class Annotate:
    def __init__(
        self,
        value: Any,
        relative_location: str,
        absolute_keyword_location: str,
    ):
        self.value = value
        self.relative_location = relative_location
        self.absolute_keyword_location = absolute_keyword_location

    def __call__(self, instance: Instance, /) -> Iterable[Evaluation]:
        yield render(self, valid=True, value=self.value, subject=instance)


class ConditionalBase:
    def __init__(
        self,
        evaluator: Evaluate,
        relative_location: str,
        absolute_keyword_location: str,
    ):
        self.evaluator = evaluator
        self.relative_location = relative_location
        self.absolute_keyword_location = absolute_keyword_location

    def __call__(self, instance: Instance, /) -> Iterable[Evaluation]:
        evaluations: list[Evaluation] = []
        evaluations += self.evaluator(instance)
        valid = not any(e.valid is False for e in evaluations)
        yield render(self, valid=valid, subject=instance, evaluations=evaluations)


class If(ConditionalBase):
    def __call__(self, instance: Instance, /) -> Iterable[Evaluation]:
        evaluations: list[Evaluation] = []
        evaluations += self.evaluator(instance)
        valid = not any(e.valid is False for e in evaluations)
        yield render(
            self, valid=True, value=valid, subject=instance, evaluations=evaluations
        )


class Then(ConditionalBase):
    pass


class Else(ConditionalBase):
    pass


class Conditional:
    def __init__(self, condition: If, when_true: Then = None, when_false: Else = None):
        self.condition = condition
        self.when_true = when_true
        self.when_false = when_false

    def __call__(self, instance: Instance, /) -> Iterable[Evaluation]:
        evaluations: list[Evaluation] = []
        evaluations += self.condition(instance)
        predicate = not any(e.value is False for e in evaluations)
        if predicate and self.when_true:
            evaluations += self.when_true(instance)
        if not predicate and self.when_false:
            evaluations += self.when_false(instance)
        yield from evaluations


class Sequence:
    def __init__(
        self,
        evaluators: list[Evaluate],
        relative_location: str,
        absolute_keyword_location: str,
    ):
        self.evaluators = evaluators
        self.relative_location = relative_location
        self.absolute_keyword_location = absolute_keyword_location

    def evaluate(self, instance: Instance, /) -> Iterable[Evaluation]:
        for evaluator in self.evaluators:
            yield from evaluator(instance)


class AllOf(Sequence):
    def __call__(self, instance: Instance, /) -> Iterable[Evaluation]:
        evaluations: list[Evaluation] = []
        evaluations += self.evaluate(instance)
        valid = not any(e.valid is False for e in evaluations)
        yield render(self, valid=valid, subject=instance, evaluations=evaluations)


class AnyOf(Sequence):
    def __call__(self, instance: Instance, /) -> Iterable[Evaluation]:
        evaluations: list[Evaluation] = []
        evaluations += self.evaluate(instance)
        valid = any(e.valid is True for e in evaluations)
        yield render(self, valid=valid, subject=instance, evaluations=evaluations)


class OneOf(Sequence):
    def __call__(self, instance: Instance, /) -> Iterable[Evaluation]:
        evaluations: list[Evaluation] = []
        evaluations += self.evaluate(instance)
        valid = sum(e.valid is True for e in evaluations) == 1
        yield render(self, valid=valid, subject=instance, evaluations=evaluations)


class Mapping:
    def __init__(
        self,
        evaluators: dict[str, Evaluate],
        relative_location: str,
        absolute_keyword_location: str,
    ):
        self.evaluators = evaluators
        self.relative_location = relative_location
        self.absolute_keyword_location = absolute_keyword_location


class Properties(Mapping):
    def __call__(self, instance: Instance[dict], /) -> Iterable[Evaluation]:
        evaluated = set()
        evaluations: list[Evaluation] = []
        for name, sub in instance:
            if name in self.evaluators:
                evaluations += self.evaluators[name](sub)
                evaluated.add(name)
        valid = not any(e.valid is False for e in evaluations)
        yield render(
            self,
            valid=valid,
            subject=instance,
            value=evaluated,
            evaluations=evaluations,
        )

    def __repr__(self):
        return f"Properties({self.evaluators!r})"


class PatternProperties(Mapping):
    def __call__(self, instance: Instance[dict], /) -> Iterable[Evaluation]:
        evaluated = set()
        evaluations: list[Evaluation] = []
        for name, sub in instance:
            for regex, evaluator in self.evaluators.items():
                if re_match(regex, name):
                    evaluations += evaluator(sub)
                    evaluated.add(name)
        valid = not any(e.valid is False for e in evaluations)
        yield render(
            self,
            valid=valid,
            subject=instance,
            value=evaluated,
            evaluations=evaluations,
        )


class AdditionalProperties:
    def __init__(
        self,
        evaluator: Evaluate,
        relative_location: str,
        absolute_keyword_location: str,
    ):
        self.evaluator = evaluator
        self.relative_location = relative_location
        self.absolute_keyword_location = absolute_keyword_location

    def __call__(
        self, instance: Instance[dict], /, *, ignore: set[str] = None
    ) -> Iterable[Evaluation]:
        evaluated: set[str] = set()
        evaluations: list[Evaluation] = []
        ignore = ignore or set()
        for name, sub in instance:
            if name in ignore:
                continue
            evaluated.add(name)
            evaluations += self.evaluator(sub)
        valid = not any(e.valid is False for e in evaluations)
        yield render(
            self,
            valid=valid,
            subject=instance,
            value=evaluated,
            evaluations=evaluations,
        )

    def __repr__(self):
        return f"AdditionalProperties({self.evaluator!r})"


class PropertiesRules:
    def __init__(
        self,
        props: Properties = None,
        pattern_props: PatternProperties = None,
        additional_props: AdditionalProperties = None,
    ):
        self.props = props
        self.pattern_props = pattern_props
        self.additional_props = additional_props

    def __call__(self, instance: Instance[dict], /) -> Iterable[Evaluation]:
        evaluations: list[Evaluation] = []
        if evaluator := cast(Evaluate, self.props):
            evaluations += evaluator(instance)
        if evaluator := cast(Evaluate, self.pattern_props):
            evaluations += evaluator(instance)
        evaluated: set[str] = extract_evaluated(evaluations, type=int)
        if additional_props := self.additional_props:
            evaluations += additional_props(instance, ignore=evaluated)
        yield from evaluations

    def __repr__(self):
        return f"PropertiesRules(props={self.props!r}, pattern_props={self.pattern_props!r}, additional_props={self.additional_props!r})"


class PropertyNames:
    def __init__(
        self,
        evaluator: Evaluate,
        relative_location: str,
        absolute_keyword_location: str,
    ):
        self.evaluator = evaluator
        self.relative_location = relative_location
        self.absolute_keyword_location = absolute_keyword_location

    def __call__(self, instance: Instance[dict], /) -> Iterable[Evaluation]:
        evaluations: list[Evaluation] = []
        for name in instance.names:
            evaluations += self.evaluator(name)
        valid = not any(e.valid is False for e in evaluations)
        yield render(self, valid=valid, subject=instance, evaluations=evaluations)


class DependentSchemas(Mapping):
    def __call__(self, instance: Instance[dict], /) -> Iterable[Evaluation]:
        evaluated = set()
        evaluations: list[Evaluation] = []
        for name, _ in instance:
            if name in self.evaluators:
                evaluations += self.evaluators[name](instance)
                evaluated.add(name)
        valid = not any(e.valid is False for e in evaluations)
        yield render(
            self,
            valid=valid,
            subject=instance,
            value=evaluated,
            evaluations=evaluations,
        )


class MinProperties:
    def __init__(
        self,
        limit: int,
        relative_location: str,
        absolute_keyword_location: str,
    ):
        self.limit = limit
        self.relative_location = relative_location
        self.absolute_keyword_location = absolute_keyword_location

    def __call__(self, instance: InstanceContext[dict], /) -> Iterable[Evaluation]:
        valid = self.limit <= len(instance.value)
        yield render(self, valid=valid, subject=instance)


class MaxProperties:
    def __init__(
        self,
        limit: int,
        relative_location: str,
        absolute_keyword_location: str,
    ):
        self.limit = limit
        self.relative_location = relative_location
        self.absolute_keyword_location = absolute_keyword_location

    def __call__(self, instance: InstanceContext[dict], /) -> Iterable[Evaluation]:
        valid = self.limit >= len(instance.value)
        yield render(self, valid=valid, subject=instance)


class MinLength:
    def __init__(
        self,
        limit: int,
        relative_location: str,
        absolute_keyword_location: str,
    ):
        self.limit = limit
        self.relative_location = relative_location
        self.absolute_keyword_location = absolute_keyword_location

    def __call__(self, instance: InstanceContext[str], /) -> Iterable[Evaluation]:
        valid = self.limit <= len(instance.value)
        yield render(self, valid=valid, subject=instance)


class MaxLength:
    def __init__(
        self,
        limit: int,
        relative_location: str,
        absolute_keyword_location: str,
    ):
        self.limit = limit
        self.relative_location = relative_location
        self.absolute_keyword_location = absolute_keyword_location

    def __call__(self, instance: InstanceContext[str], /) -> Iterable[Evaluation]:
        valid = self.limit >= len(instance.value)
        yield render(self, valid=valid, subject=instance)


class Pattern:
    def __init__(
        self,
        regex: str,
        relative_location: str,
        absolute_keyword_location: str,
    ):
        self.regex = regex
        self.relative_location = relative_location
        self.absolute_keyword_location = absolute_keyword_location

    def __call__(self, instance: InstanceContext[str], /) -> Iterable[Evaluation]:
        valid = re_match(self.regex, instance.value)
        yield render(self, valid=valid, subject=instance)


class PrefixItems:
    def __init__(
        self,
        evaluators: list[Evaluate],
        relative_location: str,
        absolute_keyword_location: str,
    ):
        self.evaluators = evaluators
        self.relative_location = relative_location
        self.absolute_keyword_location = absolute_keyword_location

    def __call__(self, instance: Instance[list], /) -> Iterable[Evaluation]:
        evaluated: set[int] = set()
        evaluations: list[Evaluation] = []
        for (i, sub), evaluator in zip(instance, self.evaluators):
            evaluated.add(cast(int, i))
            evaluations += evaluator(sub)
        valid = not any(e.valid is False for e in evaluations)
        yield render(
            self,
            valid=valid,
            subject=instance,
            value=evaluated,
            evaluations=evaluations,
        )


class AdditionalItems:
    def __init__(
        self,
        evaluator: Evaluate,
        relative_location: str,
        absolute_keyword_location: str,
    ):
        self.evaluator = evaluator
        self.relative_location = relative_location
        self.absolute_keyword_location = absolute_keyword_location

    def __call__(
        self, instance: Instance[list], /, *, ignore: set[int] = None
    ) -> Iterable[Evaluation]:
        evaluated: set[int] = set()
        evaluations: list[Evaluation] = []
        ignore = ignore or set()
        for name, sub in instance:
            if name in ignore:
                continue
            evaluated.add(name)
            evaluations += self.evaluator(sub)
        valid = not any(e.valid is False for e in evaluations)
        yield render(
            self,
            valid=valid,
            subject=instance,
            value=evaluated,
            evaluations=evaluations,
        )

    def __repr__(self):
        return f"AdditionalItems(evaluator={self.evaluator!r})"


class ItemsRules:
    def __init__(
        self,
        prefix_items: PrefixItems = None,
        additional_items: AdditionalItems = None,
    ):
        self.prefix_items = prefix_items
        self.additional_items = additional_items

    def __call__(self, instance: Instance[list], /) -> Iterable[Evaluation]:
        evaluations: list[Evaluation] = []
        if prefix_items := self.prefix_items:
            evaluations += prefix_items(instance)
        evaluated: set[int] = extract_evaluated(evaluations, type=int)
        if additional_items := self.additional_items:
            evaluations += additional_items(instance, ignore=evaluated)
        yield from evaluations

    def __repr__(self):
        return f"ItemsRules(prefix_items={self.prefix_items!r}, additional_items={self.additional_items!r})"


class MinItems:
    def __init__(
        self,
        limit: int,
        relative_location: str,
        absolute_keyword_location: str,
    ):
        self.limit = limit
        self.relative_location = relative_location
        self.absolute_keyword_location = absolute_keyword_location

    def __call__(self, instance: InstanceContext[list], /) -> Iterable[Evaluation]:
        valid = self.limit <= len(instance.value)
        yield render(self, valid=valid, subject=instance)

    def __repr__(self):
        return f"MinItems({self.limit!r})"


class MaxItems:
    def __init__(
        self,
        limit: int,
        relative_location: str,
        absolute_keyword_location: str,
    ):
        self.limit = limit
        self.relative_location = relative_location
        self.absolute_keyword_location = absolute_keyword_location

    def __call__(self, instance: InstanceContext[list], /) -> Iterable[Evaluation]:
        valid = self.limit >= len(instance.value)
        yield render(self, valid=valid, subject=instance)

    def __repr__(self):
        return f"MaxItems({self.limit!r})"


class UniqueItems:
    def __init__(
        self,
        activated: bool,
        relative_location: str,
        absolute_keyword_location: str,
    ):
        self.activated = activated
        self.relative_location = relative_location
        self.absolute_keyword_location = absolute_keyword_location

    def __call__(self, instance: InstanceContext[list], /) -> Iterable[Evaluation]:
        if self.activated:
            found = []
            valid = True
            for element in instance.value:
                e = make_comparable(element)
                if e in found:
                    valid = False
                    break
                found.append(e)
        yield render(self, valid=valid, subject=instance)


class Contains:
    def __init__(
        self,
        evaluator: Evaluate,
        relative_location: str,
        absolute_keyword_location: str,
    ):
        self.evaluator = evaluator
        self.relative_location = relative_location
        self.absolute_keyword_location = absolute_keyword_location

    def __call__(self, instance: Instance[list], /) -> Iterable[Evaluation]:
        evaluations: list[Evaluation] = []
        evaluated = set()
        for index, sub in instance:
            tmp = list(self.evaluator(sub))
            if all(t.valid is True for t in tmp):
                evaluated.add(index)
            evaluations += tmp
        valid = bool(evaluated)
        yield render(
            self,
            valid=valid,
            subject=instance,
            value=evaluated,
            evaluations=evaluations,
        )


class MinContains:
    def __init__(
        self,
        limit: int,
        relative_location: str,
        absolute_keyword_location: str,
    ):
        self.limit = limit
        self.relative_location = relative_location
        self.absolute_keyword_location = absolute_keyword_location

    def __call__(self, instance: InstanceContext[set[int]], /) -> Iterable[Evaluation]:
        valid = self.limit <= len(instance.value)
        yield render(self, valid=valid, subject=instance)


class MaxContains:
    def __init__(
        self,
        limit: int,
        relative_location: str,
        absolute_keyword_location: str,
    ):
        self.limit = limit
        self.relative_location = relative_location
        self.absolute_keyword_location = absolute_keyword_location

    def __call__(self, instance: InstanceContext[set[int]], /) -> Iterable[Evaluation]:
        valid = self.limit >= len(instance.value)
        yield render(self, valid=valid, subject=instance)


class ContainmentRules:
    def __init__(
        self,
        contains: Contains,
        minimum: MinContains = None,
        maximum: MaxContains = None,
    ):
        self.contains = contains
        self.minimum = minimum
        self.maximum = maximum

    def __call__(self, instance: Instance[list], /) -> Iterable[Evaluation]:
        evaluations: list[Evaluation] = []
        evaluations += self.contains(instance)
        yield from evaluations
        evaluated = set()
        for evaluation in evaluations:
            if evaluation.valid is True:
                evaluated.update(evaluation.value)
        if self.minimum:
            yield from self.minimum(instance.ctx(evaluated))
        if self.maximum:
            yield from self.maximum(instance.ctx(evaluated))


class UnevaluatedProperties:
    def __init__(
        self,
        evaluator: Evaluate,
        relative_location: str,
        absolute_keyword_location: str,
    ):
        self.evaluator = evaluator
        self.relative_location = relative_location
        self.absolute_keyword_location = absolute_keyword_location

    def __call__(
        self, instance: Instance[dict], /, *, ignore: set[str] = None
    ) -> Iterable[Evaluation]:
        evaluated: set[str] = set()
        evaluations: list[Evaluation] = []
        ignore = ignore or set()
        for name, sub in instance:
            if name in ignore:
                continue
            evaluated.add(name)
            evaluations += self.evaluator(sub)
        valid = not any(e.valid is False for e in evaluations)
        yield render(
            self,
            valid=valid,
            subject=instance,
            value=evaluated,
            evaluations=evaluations,
        )


class UnevaluatedItems:
    def __init__(
        self,
        evaluator: Evaluate,
        relative_location: str,
        absolute_keyword_location: str,
    ):
        self.evaluator = evaluator
        self.relative_location = relative_location
        self.absolute_keyword_location = absolute_keyword_location

    def __call__(
        self, instance: Instance[list], /, *, ignore: set[int] = None
    ) -> Iterable[Evaluation]:
        evaluated: set[int] = set()
        evaluations: list[Evaluation] = []
        ignore = ignore or set()
        for name, sub in instance:
            if name in ignore:
                continue
            evaluated.add(name)
            evaluations += self.evaluator(sub)
        valid = not any(e.valid is False for e in evaluations)
        yield render(
            self,
            valid=valid,
            subject=instance,
            value=evaluated,
            evaluations=evaluations,
        )


class Enum:
    def __init__(
        self,
        values: list[Any],
        relative_location: str,
        absolute_keyword_location: str,
    ):
        self.allowed_values = values
        self.relative_location = relative_location
        self.absolute_keyword_location = absolute_keyword_location

    def __call__(self, instance: Instance) -> Iterable[Evaluation]:
        comparable = make_comparable(instance.value)
        valid = any(comparable == make_comparable(val) for val in self.allowed_values)
        yield render(self, valid=valid, subject=instance)


class Const:
    def __init__(
        self,
        value: Any,
        relative_location: str,
        absolute_keyword_location: str,
    ):
        self.allowed_value = value
        self.relative_location = relative_location
        self.absolute_keyword_location = absolute_keyword_location

    def __call__(self, instance: Instance) -> Iterable[Evaluation]:
        valid = make_comparable(instance.value) == make_comparable(self.allowed_value)
        yield render(self, valid=valid, subject=instance)


class Required:
    def __init__(
        self,
        requirements: list[str],
        relative_location: str,
        absolute_keyword_location: str,
    ):
        self.requirements = requirements
        self.relative_location = relative_location
        self.absolute_keyword_location = absolute_keyword_location

    def __call__(self, instance: Instance[dict]) -> Iterable[Evaluation]:
        missing = set(self.requirements) - set(instance.value)
        valid = not missing
        yield render(self, valid=valid, subject=instance)

    def __repr__(self):
        return f"Required({self.requirements!r})"


class DependentRequired:
    def __init__(
        self,
        dependencies: dict[str, list[str]],
        relative_location: str,
        absolute_keyword_location: str,
    ):
        self.dependencies = dependencies
        self.relative_location = relative_location
        self.absolute_keyword_location = absolute_keyword_location

    def __call__(self, instance: Instance[dict]) -> Iterable[Evaluation]:
        missing = set()
        for key, requirements in self.dependencies.items():
            if key in instance.value:
                missing |= set(requirements) - set(instance.value)
        valid = not missing
        yield render(self, valid=valid, subject=instance)


class Maximum:
    def __init__(
        self,
        limit: float,
        relative_location: str,
        absolute_keyword_location: str,
    ):
        self.limit = limit
        self.relative_location = relative_location
        self.absolute_keyword_location = absolute_keyword_location

    def __call__(self, instance: Instance[float]) -> Iterable[Evaluation]:
        valid = self.limit >= instance.value
        yield render(self, valid=valid, subject=instance)


class ExclusiveMaximum:
    def __init__(
        self,
        limit: float,
        relative_location: str,
        absolute_keyword_location: str,
    ):
        self.limit = limit
        self.relative_location = relative_location
        self.absolute_keyword_location = absolute_keyword_location

    def __call__(self, instance: Instance[float]) -> Iterable[Evaluation]:
        valid = self.limit > instance.value
        yield render(self, valid=valid, subject=instance)


class Minimum:
    def __init__(
        self,
        limit: float,
        relative_location: str,
        absolute_keyword_location: str,
    ):
        self.limit = limit
        self.relative_location = relative_location
        self.absolute_keyword_location = absolute_keyword_location

    def __call__(self, instance: Instance[float]) -> Iterable[Evaluation]:
        valid = self.limit <= instance.value
        yield render(self, valid=valid, subject=instance)


class ExclusiveMinimum:
    def __init__(
        self,
        limit: float,
        relative_location: str,
        absolute_keyword_location: str,
    ):
        self.limit = limit
        self.relative_location = relative_location
        self.absolute_keyword_location = absolute_keyword_location

    def __call__(self, instance: Instance[float]) -> Iterable[Evaluation]:
        valid = self.limit < instance.value
        yield render(self, valid=valid, subject=instance)


class MultipleOf:
    def __init__(
        self,
        operand: float,
        relative_location: str,
        absolute_keyword_location: str,
    ):
        self.operand = operand
        self.relative_location = relative_location
        self.absolute_keyword_location = absolute_keyword_location

    def __call__(self, instance: Instance[float]) -> Iterable[Evaluation]:
        if self.operand > instance.value:
            yield render(
                self,
                valid=False,
                subject=instance,
                reason=f"Value is not a multiple of {self.operand}",
            )
        elif instance.value == self.operand:
            yield render(self, valid=True, subject=instance)
        elif instance.value % self.operand == 0:
            yield render(self, valid=True, subject=instance)
        else:
            yield render(
                self,
                valid=False,
                subject=instance,
                reason=f"Value is not a multiple of {self.operand}",
            )


class Format:
    def __init__(
        self,
        checker: Callable[[Any], bool | NotImplementedType],
        relative_location: str,
        absolute_keyword_location: str,
    ):
        self.checker = checker
        self.relative_location = relative_location
        self.absolute_keyword_location = absolute_keyword_location

    def __call__(self, instance: Instance[float]) -> Iterable[Evaluation]:
        if (valid := self.checker(instance.value)) is not NotImplemented:
            yield render(self, valid=valid, subject=instance)


class Only:
    def __init__(
        self,
        evaluators: list[Evaluate],
        type: str,
    ):
        self.evaluators = evaluators
        self.type = type

    def __call__(self, instance: Instance, /) -> Iterable[Evaluation]:
        if is_type(instance.value, self.type):
            for evaluator in self.evaluators:
                yield from evaluator(instance)

    def __repr__(self):
        return f"Only(type={self.type!r}, evaluators={self.evaluators!r})"


def extract_evaluated(evaluations: list[Evaluation], type=Type[T]) -> set[T]:
    return reduce(
        lambda a, b: a | b,
        (c.value for c in evaluations if c.valid is True),
        set(),
    )


def re_match(regex, value):
    import re

    return bool(re.search(regex, value))


from functools import singledispatch

BOOLEAN_TRUE = object()
BOOLEAN_FALSE = object()


@singledispatch
def make_comparable(obj):
    return obj


@make_comparable.register(bool)
def make_comparable_bool(obj):
    if obj is True:
        return BOOLEAN_TRUE
    if obj is False:
        return BOOLEAN_FALSE


@make_comparable.register(float)
def make_comparable_float(obj: float):
    return Decimal(str(obj))


@make_comparable.register(int)
def make_comparable_int(obj: int):
    return Decimal(obj)


@make_comparable.register(dict)
def make_comparable_dict(obj):
    return {key: make_comparable(val) for key, val in obj.items()}


@make_comparable.register(list)
def make_comparable_list(obj):
    return [make_comparable(element) for element in obj]
