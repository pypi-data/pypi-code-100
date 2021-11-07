from numpy import float64
import pandas as pd
import re

# from pandas.core.arrays.integer import Int64Dtype


class ConductivityParser:
    def __init__(self, header=["source", "target", "conductivity"]):
        self.header = header

    def run(self, filename):
        df = pd.read_table(
            filename,
            delim_whitespace=True,
            header=None,
            names=self.header,
            dtype={"source": str, "target": str, "conductivity": float64},
        )
        return df


def get_number(col):
    return int(re.sub("^0+", "", col.split("_")[0]))


def get_residue(col):
    return col.split("_")[1]


class ConductivityFormatter:
    def __init__(self):
        pass

    def run(self, df):
        df = df.copy()
        for header in ["source", "target"]:
            df[f"{header}_number"] = df[header].map(get_number)
            df[f"{header}_residue"] = df[header].map(get_residue)
        return df
