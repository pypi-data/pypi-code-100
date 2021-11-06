import pygeos

from eo_tilematcher.eo_tilematcher import intersects
import geopandas as gpd
from matplotlib import pyplot as plt


def plot_sentinel2_tiles(gdf_sentinel, figsize_=(12, 12), ax=None):
    if ax is None:
        f, ax = plt.subplots(1, 1, figsize=figsize_)
        gdf_sentinel.plot(ax=ax, facecolor="none", edgecolor="k", lw=3)
    else:
        gdf_sentinel.plot(
            ax=ax, facecolor="none", edgecolor="k", lw=3, figsize=figsize_
        )
    for index, r in gdf_sentinel.iterrows():
        geom_x, geom_y = r["geometry"].centroid.x, r["geometry"].centroid.y
        name = "Tile Name {}".format(r.Name)
        ax.text(geom_x, geom_y, name)

    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    return ax


# print(intersects("sentinel2", pygeos.creation.box(-64, -27, -66, -25))["TILE"].to_list())
# print(intersects("landsat5", pygeos.creation.box(-64, -27, -66, -25))["PATH#ROW"].to_list())
# print(intersects("landsat8", pygeos.creation.box(-64, -27, -66, -25))["PATH#ROW"].to_list())

DATA_DIR = Path(__file__).parent / "../data"

json_test_files = [
    "sentinel2",
    DATA_DIR / "ezequiel-ramos-mexia-dam.geojson",
    "landsat5",
    DATA_DIR / "ezequiel-ramos-mexia-dam.geojson",
    "landsat8",
    DATA_DIR / "ezequiel-ramos-mexia-dam.geojson",
    # DATA_DIR / "fontana-lake.geojson",
]


def test_geojson(satellite, file_path):
    gpd_roi = gpd.read_file(file_path)

    sentinel_match = intersects("sentinel2", gpd_roi)
    print(sentinel_match)


#
# print(pygeos.creation.linearrings(a[0]))
# sentinel = gpd.GeoDataFrame(
#     pygeos.creation.polygons([pygeos.creation.linearrings(a[0])])
# , columns=["geometry"]
# )
# print(sentinel)
# plot_sentinel2_tiles(sentinel)
# plt.show()
# print(sentinel)

#
# print(a[0])
#
# from pprint import pprint
#
# b = pygeos.creation.linearrings(a[0])
#
# # print(b[1])
# # print(b[0])
# pprint(dir(pygeos.creation.linearrings(a[0])))
# plt.plot()
# for pol in fiona.open('../data/sentinel2/sentinel2_tiles_world.shp'):
#     # pprint(pol)
#     print()
#     pprint(np.array(pol['geometry']["coordinates"]).squeeze())
#     print()
#     pprint(pol["properties"]["Name"])
#     break
