from argparse import ArgumentParser
from typing import IO, List

from boto3.session import Session

from stackdiff.stack_diff import StackDiff
from stackdiff.version import get_version


def entry(cli_args: List[str], writer: IO[str]) -> int:
    parser = ArgumentParser(
        description="Visualises the changes described by an Amazon Web Services CloudFormation stack change set.",
        epilog="Made with love by Cariad Eccleston: https://github.com/cariad/stackdiff",
    )

    parser.add_argument("--change", help="change set ARN, ID or name")
    parser.add_argument("--stack", help="stack ARN, ID or name")
    parser.add_argument("--version", action="store_true", help="print the version")

    args = parser.parse_args(cli_args)

    if args.version:
        writer.write(get_version() + "\n")
        return 0

    if not args.change or not args.stack:
        writer.write(parser.format_help())
        return 1

    cs = StackDiff(change=args.change, session=Session(), stack=args.stack)
    cs.render_differences(writer)
    writer.write("\n")
    cs.render_changes(writer)
    return 0
