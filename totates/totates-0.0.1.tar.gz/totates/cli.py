import argparse

from . import __version__


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--version", action="version", version=".".join(map(str, __version__))
    )
    args = p.parse_args()
