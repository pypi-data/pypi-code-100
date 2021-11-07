import unittest
import os
from click.testing import CliRunner

from canalyse.cli import conductivity


class TestCliConductivity(unittest.TestCase):
    def setUp(self) -> None:
        self.conductivity_file = (
            f"{os.path.dirname(os.path.abspath(__file__))}/assets/conductivity.dot"
        )
        self.cli = CliRunner()
        return super().setUp()

    def test_standard_deviation_grater_than(self):
        result = self.cli.invoke(
            conductivity,
            ["--quantity=std", "--grater-than", 0.004, self.conductivity_file],
        )
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(len(result.output), 0)

        result = self.cli.invoke(
            conductivity,
            ["--quantity=std", "--grater-than", 100.0, self.conductivity_file],
        )
        self.assertEqual(result.exit_code, 0)
        self.assertNotEqual(len(result.output), 0)

    def test_standard_deviation_less_than(self):
        result = self.cli.invoke(
            conductivity,
            ["--quantity=std", "--less-than", 0.005, self.conductivity_file],
        )
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(len(result.output), 0)

        result = self.cli.invoke(
            conductivity,
            ["--quantity=std", "--less-than", 0.0, self.conductivity_file],
        )
        self.assertEqual(result.exit_code, 0)
        self.assertNotEqual(len(result.output), 0)

    def test_average_grater_than(self):
        result = self.cli.invoke(
            conductivity,
            ["--quantity=average", "--grater-than", 0.01, self.conductivity_file],
        )
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(len(result.output), 0)

    def test_average_less_than(self):
        result = self.cli.invoke(
            conductivity,
            ["--quantity=average", "--less-than", 0.02, self.conductivity_file],
        )
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(len(result.output), 0)

    def test_variance_grater_than(self):
        result = self.cli.invoke(
            conductivity,
            ["--quantity=variance", "--grater-than", 2.0e-5, self.conductivity_file],
        )
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(len(result.output), 0)

    def test_variance_less_than(self):
        result = self.cli.invoke(
            conductivity,
            ["--quantity=variance", "--less-than", 2.1e-5, self.conductivity_file],
        )
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(len(result.output), 0)
