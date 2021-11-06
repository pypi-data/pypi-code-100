"""Tests for `eo_tilematcher` package."""

import geopandas as gpd
import pygeos
import pytest
from pathlib import Path

from eo_tilematcher import intersects, get_example_data

DATA_DIR = Path(__file__).parent / "../data"

test_args = [
    (
        "sentinel2",
        (-64, -27, -66, -25),
        [
            "19JGL",
            "19JGM",
            "19JGN",
            "19JHM",
            "19JHN",
            "20JKR",
            "20JKS",
            "20JKT",
            "20JLR",
            "20JLS",
            "20JLT",
            "20JMR",
            "20JMS",
        ],
    ),
    (
        "landsat5",
        (-64, -27, -66, -25),
        ["230#077", "230#078", "230#079", "231#077", "231#078", "231#079"],
    ),
    (
        "landsat8",
        (-64, -27, -66, -25),
        ["230#077", "230#078", "230#079", "231#077", "231#078", "231#079"],
    ),
]


@pytest.mark.parametrize("satellite, bbox, expected_tiles", test_args)
def test_intersect(satellite, bbox, expected_tiles):
    expected_tiles = set(expected_tiles)

    tiles = intersects(satellite, pygeos.creation.box(*bbox))

    if satellite == "sentinel2":
        tiles = set(tiles["TILE"].to_list())
    else:
        tiles = set(tiles["PATH#ROW"].to_list())

    assert tiles == expected_tiles


EXAMPLE1_FILE = get_example_data("ezequiel-ramos-mexia-dam")
EXAMPLE2_FILE = get_example_data("fontana-lake")

json_test_files = [
    ("sentinel2", EXAMPLE1_FILE, ("19HDS", "19HES")),
    ("landsat5", EXAMPLE1_FILE, "231#087"),
    ("landsat8", EXAMPLE1_FILE, "231#087"),
    ("sentinel2", EXAMPLE2_FILE, "18GYR"),
    ("landsat5", EXAMPLE2_FILE, "231#091"),
    ("landsat8", EXAMPLE2_FILE, "231#091"),
]


@pytest.mark.parametrize("satellite, file_path, expected_tiles", json_test_files)
def test_geojson(satellite, file_path, expected_tiles):
    if not isinstance(expected_tiles, (tuple, list)):
        expected_tiles = (expected_tiles,)

    gpd_roi = gpd.read_file(file_path)
    tiles = intersects(satellite, gpd_roi)
    if satellite == "sentinel2":
        tiles = set(tiles["TILE"].to_list())
    else:
        tiles = set(tiles["PATH#ROW"].to_list())
    assert set(expected_tiles) == tiles
