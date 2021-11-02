from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from .evaluators import Instance

if TYPE_CHECKING:
    from .evaluators import Evaluate, Evaluation
    from .res import Document


@dataclass
class Validation:
    valid: bool
    instance_value: Any
    evaluations: list[Evaluation]


class Validator:
    def __init__(self, doc: Document, evaluator: Evaluate):
        self.doc = doc
        self.evaluator = evaluator

    def validate(self, value: Any, /) -> Validation:
        instance = Instance("", value=value)
        evaluations: list[Evaluation] = []
        evaluations += self.evaluator(instance)
        valid = not any(e.valid is False for e in evaluations)
        return Validation(valid, instance_value=value, evaluations=evaluations)
