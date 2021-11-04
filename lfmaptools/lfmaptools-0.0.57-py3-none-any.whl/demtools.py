import os
from osgeo import gdal

def hillshade(DEMfile, outname='Hillshade.tif'):
  if outname is None:
      raise ValueError('outname must not be None')

  if not os.path.exists(DEMfile):
      raise ValueError('DEM file {} not found'.format(DEMfile))

  path = os.path.split(DEMfile)[0]

  HS = gdal.DEMProcessing(os.path.join(path, outname), DEMfile, 'hillshade', format='GTiff')
  return HS
