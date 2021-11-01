"""Implementation of individual expression types."""
import re
import typing as t

from dotty_dict import Dotty  # type: ignore

from .base import BinaryExpression  # pylint: disable=unused-import
from .base import ActionExpression, Expression, MatchExpression, UnaryExpression

################ Unary Expressions ################


class And(UnaryExpression):
    """Require all sub-expressions to be True."""

    op = "and"

    def evaluate(self, i_dict: Dotty) -> bool:
        """Evaluate ``and`` expression."""
        res = True
        for expr in self.exprs:
            if not expr.evaluate(i_dict):
                res = False
                break
        return res

    def __repr__(self):
        """Implement `repr()`."""
        return "\n\t and ".join([repr(expr) for expr in self.exprs])


class Or(UnaryExpression):
    """Require at least one sub-expression to be True."""

    op = "or"

    def evaluate(self, i_dict: Dotty) -> bool:
        """Evaluate ``or`` expression."""
        res = False
        for expr in self.exprs:
            if expr.evaluate(i_dict):
                res = True
                break
        return res

    def __repr__(self):
        """Implement `repr()`."""
        return "\n\t or ".join([repr(expr) for expr in self.exprs])


class Not(UnaryExpression):
    """Require sub-expression to be False."""

    op = "not"

    def __init__(self, exprs: t.List[Expression]) -> None:
        """Initialize Not expression.

        Args:
            exprs (t.List[Expression]): List of expressions.
        """
        if len(exprs) > 1:
            raise ValueError(
                f"Not block can only have 1 child element, found {len(exprs)}",
                "Try grouping with And or Or",
            )
        super().__init__(exprs)

    def evaluate(self, i_dict: Dotty) -> bool:
        """Evaluate ``not`` expression."""
        return not self.exprs[0].evaluate(i_dict)

    def __repr__(self):
        """Implement `repr()`."""
        return "not (\n\t" + "\n\t".join([repr(expr) for expr in self.exprs]) + "\n)"


################ Binary Expressions ################


class Contains(MatchExpression):
    """Returns True if ``value`` is in the ``field``."""

    op = "contains"

    def matches(self, i_dict: Dotty) -> bool:
        """Evaluate match."""
        val = self.get_value(i_dict)
        return self.value in val

    def __repr__(self):
        """Implement `repr()`."""
        return f"{self.value} is in {self._field}"


class Is(MatchExpression):
    """Returns True if the ``field``'s value equals ``value``."""

    op = "is"

    def matches(self, i_dict: Dotty) -> bool:
        """Evaluate match."""
        val = self.get_value(i_dict)
        return val == self.value

    def __repr__(self):
        """Implement `repr()`."""
        return f"{self._field} is {self.value}"


class In(MatchExpression):
    """Return True if ``field``'s value is in the list ``value``."""

    op = "in"

    def matches(self, i_dict: Dotty) -> bool:
        """Evaluate match."""
        val = self.get_value(i_dict)
        return val in self.value

    def __repr__(self):
        """Implement `repr()`."""
        return f"{self._field} is in {self.value}"


class Exists(MatchExpression):
    """Return True if ``field`` exists."""

    op = "exists"

    def matches(self, i_dict: Dotty) -> bool:
        """Evaluate match."""
        return self.field in i_dict if self.value else self.field not in i_dict

    def __repr__(self):
        """Implement `repr()`."""
        return self._field + (" exists" if self.value else " doesn't exist")


class Regex(MatchExpression):
    """Return True if ``field``'s value matches the regex ``value``.

    Available config options:
        case_sensitive (bool, default False): Make the regex case-sensitive.
            Defaults to case insensitive.
    """

    op = "regex"

    @staticmethod
    def validate(
        field: str,
        val: t.Any,
        variables: t.Optional[t.Dict[str, str]] = None,
        **kwargs,
    ) -> t.List[str]:
        """Validate regex config option(s)."""
        # TODO: Explain this syntax
        err = super(Regex, Regex).validate(field, val, variables, **kwargs)
        if "case_sensitive" in kwargs and not isinstance(
            kwargs["case_sensitive"], bool
        ):
            err.append(
                "Regex case-sensitive must be boolean, found "
                f"'{kwargs['case_sensitive']}'"
            )
        return err

    def matches(self, i_dict: Dotty) -> bool:
        """Evaluate match."""
        if "case_sensitive" in self.config and self.config["case_sensitive"]:
            regex = re.compile(self.value)
        else:
            regex = re.compile(self.value, re.IGNORECASE)
        val = self.get_value(i_dict)
        return bool(regex.search(val))

    def __repr__(self):
        """Implement `repr()`."""
        return f"{self._field} matches regex {self.value}"


class Startswith(MatchExpression):
    """Return True if ``field`` starts with ``value``."""

    op = "startswith"

    def matches(self, i_dict: Dotty) -> bool:
        """Evaluate match."""
        regex = re.compile(f"^{self.value}")
        val = self.get_value(i_dict)
        return bool(regex.match(val))

    def __repr__(self):
        """Implement `repr()`."""
        return f"{self._field} starts with {self.value}"


################ Action Expressions ################


class Set(ActionExpression):
    """Set ``field`` to ``value``."""

    op = "set"

    def apply(self, i_dict: Dotty) -> bool:
        """Evaluate action."""
        i_dict[self.field] = self.value
        return True

    def __repr__(self):
        """Implement `repr()`."""
        return f"set {self._field} to {self.value}"


class Add(ActionExpression):
    """Add ``value`` to ``field``.

    Available config options:
        allow_duplicate (bool, default False): Allow add to duplicate an
            existing value. Defaults to False.
    """

    op = "add"

    @staticmethod
    def validate(
        field: str,
        val: t.Any,
        variables: t.Optional[t.Dict[str, str]] = None,
        **kwargs,
    ) -> t.List[str]:
        """Validate `allow_duplicate` for regex."""
        # err = super().validate(field, val, variables, **kwargs) returns a
        # mypy error: error: Argument 2 for "super" not an instance of
        # argument 1
        # My understanding is that super() is calling an instance method
        # In order to call a static method, you need super(cls, cls)
        err = super(Add, Add).validate(field, val, variables, **kwargs)
        if "allow_duplicate" in kwargs and not isinstance(
            kwargs["allow_duplicate"], bool
        ):
            err.append(
                "Add allow-duplicate must be boolean, found "
                f"'{kwargs['allow_duplicate']}'"
            )
        return err

    def apply(self, i_dict: Dotty) -> bool:
        """Evaluate action."""
        duplicate = "allow_duplicate" in self.config and self.config["allow_duplicate"]
        # Adder only if to_add is not already in existing, or config marks
        #   specifically to allow duplicating values.
        _add = lambda existing, to_add: (
            (to_add not in existing or duplicate) and existing.append(to_add)
        )
        val = i_dict.get(self.field, [])
        if isinstance(self.value, list):
            for v in self.value:
                _add(val, v)
        else:
            _add(val, self.value)
        i_dict[self.field] = val
        return True

    def __repr__(self):
        """Implement `repr()`."""
        return f"add {self.value} to {self._field}"
