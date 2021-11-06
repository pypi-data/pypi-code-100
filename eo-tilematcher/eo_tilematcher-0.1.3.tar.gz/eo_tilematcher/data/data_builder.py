"""
Script used to build the tiles databases for the Sentinel2,
Landsat5, and Landsat8 spacecrafts.
"""
import os
import geopandas as gpd
from pathlib import Path


def build_sentinel2_db():
    """Extract the Sentinel2 tiles information and store it in pickle format."""
    data_dir = Path(__file__).parent
    wrs_file = os.path.join(
        data_dir, "./sentinel2/sentinel2_tiles_world.zip!sentinel2_tiles_world.shp"
    )
    gpd_ = gpd.read_file(wrs_file)
    gpd_.columns = ["TILE", "geometry"]
    gpd_.to_file(
        os.path.join(data_dir, "sentinel2/sentinel2_tiles.shp"), driver="ESRI Shapefile"
    )
    gpd_ = None


def build_lansat_db():
    """Extract the Landsat tiles (path/row) information and store it in pickle format."""
    data_dir = Path(__file__).parent
    wrs_file = os.path.join(
        data_dir, "landsat/WRS2_descending_0.zip!WRS2_descending.shp"
    )
    gpd_ = gpd.read_file(wrs_file)
    gpd_["PATH#ROW"] = (
        gpd_["PATH"].apply(lambda x: f"{x:003d}")
        + "#"
        + gpd_["ROW"].apply(lambda x: f"{x:003d}")
    )
    gpd_[["PATH#ROW", "geometry"]].to_file(
        os.path.join(data_dir, "landsat/landsat_tiles.shp"), driver="ESRI Shapefile"
    )
    gpd_ = None


if __name__ == "__main__":
    build_sentinel2_db()
    build_lansat_db()
