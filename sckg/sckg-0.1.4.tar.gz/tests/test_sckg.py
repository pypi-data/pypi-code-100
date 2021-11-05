#!/usr/bin/env python

"""Tests for `sckg` package."""

import unittest
from click.testing import CliRunner

from sckg import sckg
from sckg import cli
from sckg.graph import SoftwareKG
from util.path_util import PathUtil


class TestSckg(unittest.TestCase):
    """Tests for `sckg` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'sckg.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output

    def test_get_node_info_by_id(self):
        graph_path = PathUtil.graph_data("KG", "V2.5.31")
        sckg = SoftwareKG(graph_path)
        print(sckg.get_node_info_by_id(2724))
        print(sckg.get_node_info_by_id(2724)['properties']['concept_name'])

    def test_is_exit_facet_of_relation(self):
        graph_path = PathUtil.graph_data("KG", "V2.5.31")
        sckg = SoftwareKG(graph_path)
        assert sckg.is_exit_facet_of_relation("java", "java ee") == True

    def test_is_exit_relation(self):
        graph_path = PathUtil.graph_data("KG", "V2.5.31")
        sckg = SoftwareKG(graph_path)
        assert sckg.is_exit_relation("java", "java ee") == True

    def test_find_common_out_relationship_node(self):
        graph_path = PathUtil.graph_data("KG", "V2.5.31")
        sckg = SoftwareKG(graph_path)
        print(sckg.find_common_out_relationship_node("java jdk", "java ee"))

    def test_find_out_is_a_relation_concept(self):
        graph_path = PathUtil.graph_data("KG", "V2.5.31")
        sckg = SoftwareKG(graph_path)
        print(sckg.find_out_is_a_relation_concept("java jdk"))

    def test_find_common_in_relationship_node(self):
        graph_path = PathUtil.graph_data("KG", "V2.5.31")
        sckg = SoftwareKG(graph_path)
        print(sckg.find_common_in_relationship_node("java", "java ee"))
