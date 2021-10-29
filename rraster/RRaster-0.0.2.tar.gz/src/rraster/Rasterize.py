import geopandas as gpd
import numpy as np
from pathlib import Path
import rasterio as rio
from rasterio import features
from typing import Union

def rasterize(shp: Union[str, Path], f_name: Union[str, Path], template: Union[str, Path]='./src/rraster/data/template.tif', colname: str='DM', crs: int=None):
    """
    Convert a vector shapefile to raster format based on a template raster. 
    methodology borrowed from https://gis.stackexchange.com/questions/151339/rasterize-a-shapefile-with-geopandas-or-fiona-python/151861

    :param shp: Path to the shapefile that will be rasterized. 
    :param f_name: The full path and name for the file that will be saved out.
    :param template: The raster template to align the shapefile with.
    :param colname: The column name in the shapefile that should be used for rasterization.
    :param crs: The EPSG code of the template that the shapefile will be transformed to. 
    :returns None: Saves out the rasterized shapefile to f_name.
    """


    # Read and reproject shapefile if necessary.
    shp = gpd.read_file(shp)
    if crs is not None:
        shp = shp.to_crs(crs)

    # Read template raster and get metadata.
    template = rio.open(template)
    meta = template.meta.copy()
    meta.update(compress='lzw')

    # Rasterize and save out new raster.
    with rio.open(f_name, 'w+', **meta) as out:

        arr = out.read(1)
        shapes = ((geom,value) for geom, value in zip(shp.geometry, shp[colname]))

        shp_as_rst = features.rasterize(shapes=shapes, fill=np.nan, out=arr, transform=out.transform)
        # TODO: Figure out why rasterio ouputs -3.4e+38 rather than the specified fill value.
        shp_as_rst[shp_as_rst == np.float32(-3.4e+38)] = np.nan

        out.write_band(1, shp_as_rst)
    