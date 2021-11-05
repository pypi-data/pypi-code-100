"""Main CLI code."""
import argparse
import configparser
import sys
from pathlib import Path
from typing import Optional
from typing import Sequence


def print_connection_string(config_name: str) -> int:
    """Print connection string using supplied config name.

    Args:
        config_name (str): Name of config in `.usql_conf`.

    Returns:
        int: Return value of command.
    """
    local_config_path = Path().cwd() / ".usql_conf"
    global_config_path = Path().home() / ".usql_conf"

    if local_config_path.exists():
        local_config_parser = configparser.ConfigParser()
        local_config_parser.read(local_config_path)
        try:
            local_connection_string = local_config_parser.get(
                config_name,
                "connection_string",
            )
        except configparser.NoSectionError:
            local_connection_string = ""
    else:
        local_connection_string = ""

    if global_config_path.exists():
        global_config_parser = configparser.ConfigParser()
        global_config_parser.read(global_config_path)
        try:
            global_connection_string = global_config_parser.get(
                config_name,
                "connection_string",
            )
        except configparser.NoSectionError:
            global_connection_string = ""
    else:
        global_connection_string = ""

    if local_connection_string:
        print(local_connection_string)
        return 0
    elif global_connection_string:
        print(global_connection_string)
        return 0
    else:
        print(f"Config '{config_name}' has not been set in .usql_conf", file=sys.stderr)
        return 1


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Entry-point for `usql_conf` CLI."""
    parser = argparse.ArgumentParser()
    parser.add_argument("config_name")
    args = parser.parse_args(argv)

    return_value = print_connection_string(args.config_name)

    return return_value


if __name__ == "__main__":
    raise SystemExit(main())
