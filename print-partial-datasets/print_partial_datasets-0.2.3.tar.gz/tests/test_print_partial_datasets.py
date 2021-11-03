#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for print_partial_datasets_package

Created on Sun Nov 29 11:39:58 2020

@author: evan
"""

import sys
from argparse import Namespace
import pytest
from pathlib import Path
from print_partial_datasets import cli
from print_partial_datasets import print_partial_datasets
from unittest.mock import patch


@pytest.fixture(scope="module")
def datadir():
    return Path("tests/testdata/")


@pytest.fixture(scope="module")
def treepath():
    return Path("print_partial_datasets/file_tree/biomox.tree")


def test_out_txt(capsys, datadir, treepath):
    """Test against sample dataset"""
    knowntext = (
        Path("tests/testdata/test_print_table.txt").open("r").read()
    )
    # Capture stdout
    print_partial_datasets(
        datadir,
        treepath,
        ["raw_T1", "raw_bold", "raw_fmap_mag", "raw_fmap_ph"],
        ["participant"],
        session=["01", "02"],
    )
    captured = capsys.readouterr()

    assert captured.out == knowntext


@patch("print_partial_datasets.cli.print_partial_datasets")
def test_main(mock_ppd):
    with patch.object(
        sys,
        "argv",
        "./cli.py -d /path/to/dir -f print_partial_datasets/file_tree/biomox.tree -s raw_T1 raw_bold -v participant session".split(),
    ):
        cli.main()
        mock_ppd.assert_called_once_with(
            "/path/to/dir",
            "print_partial_datasets/file_tree/biomox.tree",
            ["raw_T1", "raw_bold"],
            ["participant", "session"],
        )

def test_noargs():
    with pytest.raises(SystemExit):
        with patch.object(sys, "argv", ["./print_filetree_table.py"]):
            cli.main()
