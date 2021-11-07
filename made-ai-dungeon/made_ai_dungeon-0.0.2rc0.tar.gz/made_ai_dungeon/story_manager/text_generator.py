from typing import Protocol, Any


class TextGenerator(Protocol):
    def generate_text(self, input_text: str, context: Any) -> tuple[str, Any]:
        ...
