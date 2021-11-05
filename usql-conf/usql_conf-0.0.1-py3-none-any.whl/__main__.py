"""Alternate CLI entry-point via `python -m usql_conf`"""
from usql_conf.cli import main

if __name__ == '__main__':
    raise SystemExit(main())
