import argparse
import geopandas as gpd
from eo_tilematcher import intersects


def match_tiles():
    parser = argparse.ArgumentParser(description="EO-tilematcher")
    # mandatory
    parser.add_argument(
        "roi", type=str, help="ROI FILE (any file that fiona/geopandas can open)"
    )
    # optional
    parser.add_argument(
        "--spacecraft",
        type=str,
        help="satellite (landsat5,landsat8,sentinel2)",
        default="sentinel2",
    )
    parser.add_argument(
        "--verbose", help="Display results (if any)", action="store_true"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output file path where the results are saved (GPKG driver). "
        "If it is not specified, the results are printed to the screen.",
    )

    m, _ = parser.parse_known_args()
    bbox = gpd.read_file(m.roi)
    tiles_match = intersects(m.spacecraft, bbox)
    if m.output is None:
        m.verbose = True

    if m.verbose:
        if tiles_match.shape[0] > 0:
            print(tiles_match)
        else:
            print("Could not find any intersection")
    if m.output is not None:
        if tiles_match.shape[0] > 0:
            tiles_match.to_file(m.output, driver="GPKG")


match_tiles()
