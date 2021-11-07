def add_surrogates(text: str) -> bytes:
    return text.encode("utf-16-le")


def remove_surrogates(text: bytes) -> str:
    return text.decode("utf-16-le")