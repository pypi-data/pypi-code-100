import argparse
import os
import sys


if sys.platform == 'win32':  # pragma: win32 no cover
    import subprocess

    def execvp(cmd: str, args: 'list[str]') -> int:
        return subprocess.call(args)
else:  # pragma: posix no cover
    from os import execvp


def venv_is_active() -> bool:
    return True if os.environ.get("VIRTUAL_ENV", None) else False


def main() -> int:

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--allow-no-venv",
                        action="store_true",
                        help="Install packages without checking whether a venv is activated.")
    parser.add_argument("--help", action="store_true", help="Show help")

    args, rest = parser.parse_known_args()

    if args.help:
        parser.print_help()

        print()
        print("pip3 --help")
        print("=" * 79)
        cmd = ["pip3", "--help"]
        return execvp(cmd[0], cmd)

    elif venv_is_active() or args.allow_no_venv:
        cmd = ["pip3", *rest]
        return execvp(cmd[0], cmd)

    else:
        if len(rest) >= 1:
            if rest[0] == "install":
                print("Activate your venv kiddo!", file=sys.stderr)
                return 1

            else:
                cmd = ["pip3", *rest]
                return execvp(cmd[0], cmd)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
