from typing import Any
from typing_extensions import Protocol


class TextGenerator(Protocol):
    def generate_text(self, input_text: str, context: Any) -> tuple[str, Any]:
        ...
