"""
Eo-tilematcher package.
"""

import geopandas as gpd
import pandas as pd
import pygeos
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"


def _db_loader(file_name):
    subdir = file_name.split("_")[0]
    tiles_db = gpd.read_file(DATA_DIR / subdir / file_name, driver="ESRI Shapefile")
    return tiles_db


def _sentinel2_db_loader():
    return _db_loader("sentinel2_tiles.shp")


def _landsat_db_loader():
    return _db_loader("landsat_tiles.shp")


SPACECRAFTS_DB = dict(
    sentinel2=None,
    landsat5=None,
    landsat8=None,
)

SPACECRAFTS_LOADERS = dict(
    sentinel2=_sentinel2_db_loader,
    landsat5=_landsat_db_loader,
    landsat8=_landsat_db_loader,
)


def get_spacecraft_db(spacecraft):
    spacecraft = spacecraft.lower()
    if spacecraft not in SPACECRAFTS_DB:
        raise ValueError(
            f"Spacecraft '{spacecraft}' not supported.\n"
            f"Allowed values: {str(list(SPACECRAFTS_DB.keys()))}"
        )

    if SPACECRAFTS_DB[spacecraft] is None:
        SPACECRAFTS_DB[spacecraft] = SPACECRAFTS_LOADERS[spacecraft]()
    return SPACECRAFTS_DB[spacecraft]


def get_contains_intersect_on_tiles(gpd_to_match, gpd_tiles, gpd_tiles_col):
    """get if contains or intersects (but not contains) shape on sat tiles
    Parameters
    ----------
        gpd_to_match: geodataframe
            roi to be intersected by tiles
        gpd_tiles: geodataframe
            geodataframe of sat tiles or path#rows
        gpd_tiles_col: str
            tiles/pathrow column on gpd_tiles

    Returns
    -------
        geodataframe that matches shapes to tiles (either contains or
        intersects)
    """
    contains_ = []
    intersects_ = []
    tile_name_out = gpd_tiles_col
    gpd_to_match = gpd_to_match.reset_index(drop=True)

    for i, r in gpd_to_match.iterrows():
        # get those that contains geom
        flag_cont = gpd_tiles.geometry.contains(r["geometry"])
        flag_int = gpd_tiles.geometry.intersects(r["geometry"])
        if any(flag_cont):
            # any contains
            gpd_tf = gpd_tiles[flag_cont]
            for it, rt in gpd_tf.iterrows():
                gpd_ = gpd_to_match.iloc[[i]].copy()
                gpd_["match_polygon"] = rt["geometry"].intersection(r["geometry"]).wkt
                gpd_["match"] = "total"
                gpd_[tile_name_out] = rt[gpd_tiles_col]
                contains_.append(gpd_)
        elif any(flag_int):
            gpd_tf = gpd_tiles[flag_int]
            for it, rt in gpd_tf.iterrows():
                gpd_ = gpd_to_match.iloc[[i]].copy()
                gpd_["match_polygon"] = rt["geometry"].intersection(r["geometry"]).wkt
                gpd_["match"] = "partial"
                gpd_[tile_name_out] = rt[gpd_tiles_col]
                intersects_.append(gpd_)
        else:
            # switch to overlay
            gpd_test = gpd_to_match.iloc[[i]].copy()
            gpd_over = gpd.overlay(gpd_test, gpd_tiles)
            for io, ro in gpd_over.iterrows():
                gpd_tf = gpd_tiles[gpd_tiles[gpd_tiles_col] == ro[gpd_tiles_col]]
                for it, rt in gpd_tf.iterrows():
                    gpd_ = gpd_to_match.iloc[[i]]
                    # by construction
                    if rt["geometry"].contains(r["geometry"]):
                        gpd_["match_polygon"] = (
                            rt["geometry"].intersection(r["geometry"]).wkt
                        )
                        gpd_["match"] = "total-overlay"
                        gpd_[tile_name_out] = rt[gpd_tiles_col]
                        contains_.append(gpd_)
                    elif rt["geometry"].intersects(r["geometry"]):
                        gpd_["match_polygon"] = (
                            rt["geometry"].intersection(r["geometry"]).wkt
                        )
                        gpd_["match"] = "partial-overlay"
                        gpd_[tile_name_out] = rt[gpd_tiles_col]
                        intersects_.append(gpd_)
                    else:
                        raise ("Could not make any match")

    if len(contains_) and len(intersects_):
        gpd_contains_, gpd_intersects_ = pd.concat(
            contains_, ignore_index=True
        ), pd.concat(intersects_, ignore_index=True)
        gpd_contains_intersects_ = pd.concat(
            [gpd_contains_, gpd_intersects_], ignore_index=True
        )
        return gpd_contains_intersects_
    elif len(contains_) > 0:
        gpd_contains_ = pd.concat(contains_, ignore_index=True)
        return gpd_contains_
    elif len(intersects_) > 0:
        gpd_intersects_ = pd.concat(intersects_, ignore_index=True)
        return gpd_intersects_
    else:
        return gpd.GeoDataFrame()


def intersects(spacecraft, gpd_roi):
    """
    Returns the names and the geometries of the tiles that intersects a given
    Region of Interest (ROI).
    """
    if isinstance(gpd_roi, pygeos.lib.Geometry):
        gpd_roi = gpd.GeoDataFrame([gpd_roi], columns=["geometry"])

    selected_db = get_spacecraft_db(spacecraft)
    if spacecraft == "sentinel2":
        gpd_col = "TILE"
    else:
        gpd_col = "PATH#ROW"
    # get roi
    gpd_to_match = gpd_roi.copy()

    return get_contains_intersect_on_tiles(gpd_to_match, selected_db, gpd_col)


DATA_DIR = Path(__file__).parent / "data"
EXAMPLE_FILES = {
    "ezequiel-ramos-mexia-dam": DATA_DIR / "ezequiel-ramos-mexia-dam.geojson",
    "ezequiel-dam": DATA_DIR / "ezequiel-ramos-mexia-dam.geojson",
    "fontana-lake": DATA_DIR / "fontana-lake.geojson",
}


def get_example_data(name):
    name = name.lower()
    if name not in EXAMPLE_FILES:
        raise ValueError(
            f'The example file "{name}" was not found.\n'
            f"The available options are: {str(EXAMPLE_FILES.keys())}"
        )
    return EXAMPLE_FILES[name]
