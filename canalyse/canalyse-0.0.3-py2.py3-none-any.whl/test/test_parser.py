import unittest
import os
import pandas as pd
from pandas._testing import assert_frame_equal
from canalyse.parser import ConductivityParser, ConductivityFormatter


class TestParser(unittest.TestCase):
    def setUp(self) -> None:
        self.conductivity_file = (
            f"{os.path.dirname(os.path.abspath(__file__))}/assets/conductivity.dot"
        )
        return super().setUp()

    def test_conductivity_parser(self):
        parser = ConductivityParser()

        df = parser.run(self.conductivity_file)
        # Has header expected
        reference_header = ["source", "target", "conductivity"]
        assert all(df.columns == reference_header)

    def test_conductivity_formatter(self):
        parser = ConductivityParser()
        df = parser.run(self.conductivity_file)
        formatter = ConductivityFormatter()
        new_df = formatter.run(df)
        reference_df = pd.DataFrame(
            {
                "source": ["00001_MET", "00001_MET", "00001_MET"],
                "target": ["00036_PHE", "00005_GLU", "00004_ASP"],
                "conductivity": [
                    float(0.0174476321812),
                    float(0.0214987056692),
                    float(0.0124389690164),
                ],
                "source_number": [1, 1, 1],
                "source_residue": ["MET", "MET", "MET"],
                "target_number": [36, 5, 4],
                "target_residue": ["PHE", "GLU", "ASP"],
            }
        )
        assert_frame_equal(new_df, reference_df)
