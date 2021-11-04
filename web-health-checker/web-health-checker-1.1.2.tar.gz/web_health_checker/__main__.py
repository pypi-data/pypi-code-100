import sys
from argparse import ArgumentParser, Namespace

import requests
from requests.exceptions import (ConnectionError, HTTPError, Timeout,
                                 TooManyRedirects)


def eprint(*values: object):
    print(*values, file=sys.stderr)


def parse_args():
    parser = ArgumentParser(description="Health check website")
    parser.add_argument(
        "url", type=str,
        help="url to query for status"
    )
    parser.add_argument(
        "--timeout", dest="timeout",
        type=float, default=0.3,
        help="timeout before connection fail"
    )
    return parser.parse_args()


def main(args: Namespace):
    try:
        req = requests.get(
            args.url,
            timeout=args.timeout,
            allow_redirects=False
        )
        req.raise_for_status()
    except HTTPError:
        eprint(f"⛔ http status '{req.status_code}'")
    except ConnectionError:
        eprint("⛔ connection error")
    except Timeout:
        eprint("⛔ timeout error")
    except TooManyRedirects:
        eprint("⛔ to many redirects")
    else:
        print("🆗")
        return

    exit(1)


if __name__ == "__main__":
    args = parse_args()
    main(args)
