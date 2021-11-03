#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 17:30:55 2020

@author: evan
"""
import argparse
import sys

from print_partial_datasets import print_partial_datasets


def main():
    """Console script for print_partial_datasets."""
    parser = argparse.ArgumentParser(
        description="""Search a structured data directory using a ``FileTree``, producing a table
    of complete and partial datasets."""
    )
    requiredNamed = parser.add_argument_group("Required named arguments")
    requiredNamed.add_argument(
        "-d",
        "--datadir",
        nargs=1,
        help="Path to data directory",
        required=True,
    )
    requiredNamed.add_argument(
        "-f",
        "--filetree",
        nargs=1,
        help="Path to .tree file. You can specify your own, or use the default trees in fslpy, e.g. 'bids_raw', 'HCP_directory'",
        required=True,
    )
    requiredNamed.add_argument(
        "-s",
        "--short_name",
        nargs="*",
        help="A list of short names from file tree that will be searched for. e.g. raw_T1, raw_bold.",
        required=True,
    )
    requiredNamed.add_argument(
        "-v",
        "--variables",
        nargs="*",
        help="A list of variable fields - a subset of those specified in the file tree e.g. participant, session, run",
        required=True,
    )

    args = parser.parse_args()

    print_partial_datasets(
        args.datadir[0],
        args.filetree[0],
        args.short_name,
        args.variables,
    )

    return 0


if __name__ == "__main__":
    main()  # pragma: no cover
