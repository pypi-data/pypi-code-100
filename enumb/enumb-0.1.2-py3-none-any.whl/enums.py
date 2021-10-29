import case
import export

from . import bases
from . import generators
from . import utils

@export
class Name(bases.StrEnum): pass

@export
class Index(bases.IntEnum): pass

@export
class Integer(bases.IntEnum):
    _generate_next_value_ = utils.compose(generators.count, lambda count: count + 1)

@export
class NoValue(bases.Enum):
    def __repr__(self) -> str:
        return f'<{type(self).__name__}.{self.name}>'

    @property
    def value(self) -> None:
        raise AttributeError(f'{type(self).__name__!r} object has no attribute \'value\'')

@export
class Lower(bases.StrEnum):
    _generate_next_value_ = utils.compose(generators.name, case.lower)

@export
class Upper(bases.StrEnum):
    _generate_next_value_ = utils.compose(generators.name, case.upper)

@export
class Title(bases.StrEnum):
    _generate_next_value_ = utils.compose(generators.name, case.title)

@export
class Sentence(bases.StrEnum):
    _generate_next_value_ = utils.compose(generators.name, case.sentence)

@export
class Snake(bases.StrEnum):
    _generate_next_value_ = utils.compose(generators.name, case.snake)

@export
class Helter(bases.StrEnum):
    _generate_next_value_ = utils.compose(generators.name, case.helter)

@export
class Macro(bases.StrEnum):
    _generate_next_value_ = utils.compose(generators.name, case.macro)

@export
class Flat(bases.StrEnum):
    _generate_next_value_ = utils.compose(generators.name, case.flat)

@export
class Flush(bases.StrEnum):
    _generate_next_value_ = utils.compose(generators.name, case.flush)

@export
class Camel(bases.StrEnum):
    _generate_next_value_ = utils.compose(generators.name, case.camel)

@export
class Pascal(bases.StrEnum):
    _generate_next_value_ = utils.compose(generators.name, case.pascal)

@export
class Kebab(bases.StrEnum):
    _generate_next_value_ = utils.compose(generators.name, case.kebab)

@export
class Train(bases.StrEnum):
    _generate_next_value_ = utils.compose(generators.name, case.train)

@export
class Cobol(bases.StrEnum):
    _generate_next_value_ = utils.compose(generators.name, case.cobol)

@export
class Dot(bases.StrEnum):
    _generate_next_value_ = utils.compose(generators.name, case.dot)

@export
class Path(bases.StrEnum):
    _generate_next_value_ = utils.compose(generators.name, case.path)
