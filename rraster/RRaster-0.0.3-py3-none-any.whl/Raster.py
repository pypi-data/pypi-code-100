from __future__ import annotations

import copy
import tempfile
from pathlib import Path
from typing import List, Union

import matplotlib.pyplot as plt
import numpy as np
import rasterio as rio
import xarray
from rasterio.warp import Resampling, reproject


class Raster(object):
    """
    Wrapper around rasterio functions to have simpler syntax and match the logic used by the R Raster library.
    A raster can either be read from disk or created from a numpy array with an affine transformation and nodata
    value specification.

    Attributes:
        arr: array containing the raster data
        nodata: The no data value of the raster.
        transform: The affine transformation of the raster.
        profile: All other associated raster metadata.
    """

    def __init__(self, rst: Union[np.ndarray, str, Path], band: Union[int, List[int]] = 1, **kwargs):

        # Instantiate from raster on disk.
        if isinstance(rst, (str, Path)):
            rst = Path(rst)
            if not rst.exists():
                raise FileNotFoundError(f'Error! The provided raster ({rst}) does not exist.')


            with rio.open(rst) as tmp:
                self.arr = tmp.read(band)
                self.nodata = tmp.nodata
                self.arr = self.arr.astype(np.float32)
                self.arr[self.arr == tmp.nodata] = np.nan
                self.arr = self.arr * tmp.scales if tmp.scales else self.arr
                self.arr = self.arr + tmp.offsets if tmp.offsets else self.arr 
                self.bounds = tmp.bounds
                self.count = tmp.count
                self.crs = tmp.crs
                self.driver = tmp.driver or 'GTiff'
                self.dtype = tmp.profile['dtype']
                self.height = tmp.height
                self.transform = tmp.transform
                self.width = tmp.width
            
            self.name = rst.stem

        # Instantiate from np array.
        elif isinstance(rst, np.ndarray):

            assert all([x in kwargs for x in ['nodata', 'transform']]), "'nodata' and 'transform' must both be kwargs" \
                                                                        "when creating a raster from an array."

            self.arr = rst
            self.arr = self.arr.astype(np.float32)
            self.count = 1 if np.ndim(self.arr) == 2 else self.arr.shape[0]
            self.crs = None if 'crs' not in kwargs else kwargs['crs']
            self.driver = 'GTiff' if 'driver' not in kwargs else kwargs['driver']
            self.dtype = 'float32' if 'dtype' not in kwargs else kwargs['dtype']
            self.height = self.arr.shape[-2]
            self.name = 'raster_layer' if 'name' not in kwargs else kwargs['name']
            self.nodata = -9999 if 'nodata' not in kwargs else kwargs['nodata']
            self.transform = None if 'transform' not in kwargs else kwargs['transform']
            self.width = self.arr.shape[-1]

        else:
            raise TypeError('Error! "rst" must be a np.array, str or Path object')

        # Map str of data types to actual data types
        self.dt_map = {
            'float32': np.float32,
            'float64': np.float64,
            'int8': np.int8,
            'int16': np.int16
        }

        self.inv_dt_map = {self.dt_map[k] : k for k in self.dt_map}
    
    def crop(self, other: Union[List[float], Raster]):
        raise NotImplementedError('The crop method is not implemented yet.')

    def plot(self):
        """
        Simple display of the raster using matplotlib.
        """
        # Copy raster so we can filter out nodata values without changing the array already in memory.
        tmp = self.arr.copy()
        tmp = tmp.astype(np.float32)
        tmp[tmp == self.nodata] = np.nan

        plt.imshow(tmp)
        plt.colorbar()
        plt.show()

    def write(self, save_name: Union[str, Path]):
        """
        Write raster to disk.
        :param save_name: Desired path and filename of
        :param kwargs: Additional kwargs to pass to rio.open function.
        :return: None, saves raster to disk.
        """

        out_dst = rio.open(
            save_name,
            'w',
            driver='GTiff',
            height=self.height,
            width=self.width,
            count=self.count,
            dtype=self.dtype,
            nodata=self.nodata,
            transform=self.transform,
            crs=self.crs,
        )

        dt = self.dt_map[self.dtype] 

        arr = np.nan_to_num(self.arr, nan=self.nodata)
        if self.count == 1:
            out_dst.write(arr.astype(dt)[np.newaxis])
        else:
            out_dst.write(arr.astype(dt))

        out_dst.close()

    def crop(self, other: Union[Raster, List[float], rio.coords.BoundsingBox]):
        raise NotImplementedError('This function has not been implemented yet!')

    def reproject(self, other: Raster, method: str = 'bilinear', crs=None):
        """
        :param other: Raster object with the desired CRS and spatial resolution. The source raster will be
        transformed to match this raster's projection.
        :param method: The reprojection method to use. Must be one of 'bilinear', 'nearest', or 'cubic'.
        :param crs: The CRS of the source raster. If CRS is none, it is assumed that it is WGS84 (EPSG:4326).
        """
        if crs is None:
            crs = {'init': 'EPSG:4326'}

        assert method in ['nearest', 'bilinear', 'cubic'], 'Error! method must be one of "nearest", "bilinear", ' \
                                                           'or "cubic". '
        methods = {
            'nearest': Resampling.nearest,
            'bilinear': Resampling.bilinear,
            'cubic': Resampling.cubic
        }

        dst = np.zeros_like(other.arr, dtype=np.float32)
        arr, transform = reproject(
            self.arr,
            dst,
            src_transform=self.transform,
            src_crs=self.crs if self.crs is not None else crs,
            dst_transform=other.transform,
            dst_crs=other.crs,
            dst_nodata=np.nan,
            resampling=methods[method])

        return Raster(
            rst=arr, transform=transform, nodata=self.nodata, crs=other.crs,
            bounds=other.bounds, dtype=self.dtype, name=self.name, driver=self.driver
        )

    def copy(self):
        return copy.deepcopy(self)

    #TODO: Finish changing reliance on proile. 
    def __add__(self, other: Union[Raster, int, float]):
        if isinstance(other, Raster):
            assert self.arr.shape == other.arr.shape, f'Error! Rasters have different shapes. Raster 1 has shape ' \
                                                      f'{self.arr.shape} and raster 2 has shape {other.arr.shape}'
            tmp = self.arr + other.arr
        else:
            tmp = self.arr + other
        
        cp = self.copy()
        cp.arr = tmp
        return cp

    def __mul__(self, other: Union[Raster, int, float]):
        if isinstance(other, Raster):
            assert self.arr.shape == other.arr.shape, f'Error! Rasters have different shapes. Raster 1 has shape ' \
                                                      f'{self.arr.shape} and raster 2 has shape {other.arr.shape}'
            tmp = self.arr * other.arr
        else:
            tmp = self.arr * other

        cp = self.copy()
        cp.arr = tmp
        return cp

    def __sub__(self, other: Union[Raster, int, float]):
        if isinstance(other, Raster):
            assert self.arr.shape == other.arr.shape, f'Error! Rasters have different shapes. Raster 1 has shape ' \
                                                      f'{self.arr.shape} and raster 2 has shape {other.arr.shape}'
            tmp = self.arr - other.arr
        else:
            tmp = self.arr - other
        
        cp = self.copy()
        cp.arr = tmp
        return cp

    def __truediv__(self, other: Union[Raster, int, float]):
        if isinstance(other, Raster):
            assert self.arr.shape == other.arr.shape, f'Error! Rasters have different shapes. Raster 1 has shape ' \
                                                      f'{self.arr.shape} and raster 2 has shape {other.arr.shape}'
            tmp = self.arr / other.arr
        else:
            tmp = self.arr / other

        cp = self.copy()
        cp.arr = tmp
        return cp

    def __repr__(self):
        return f"raster of size {self.height} x {self.width}\ncrs: {self.crs}\n" \
               f"number of bands: {self.count} "


class RasterStack(object):
    """
    Class to handle multiple Raster objects.

    Attributes:
        rasters: List of Raster objects (all rasters should share nodata, affine and transform attributes).
        nodata: The no data value of the raster objects.
        transform: Affine transformation for all rasters.
        profile: All other raster metadata.
    """

    def __init__(self, *args, build_arr=True):
        assert all([isinstance(x, (str, Path, Raster)) for x in args]), 'Error! All rasters must be the same format.'
        if not isinstance(args[0], Raster):
            args = [Raster(x) for x in args]

        self.rasters = args        

        self.crs = self.rasters[0].crs or None
        self.driver = self.rasters[0].driver or 'GTiff' 
        self.dtype = self.rasters[0].dtype or 'float32' 
        self.height = self.rasters[0].height
        self.names = [x.name for x in self.rasters]
        self.nodata = self.rasters[0].nodata or -9999 
        self.transform = self.rasters[0].transform or None
        self.width = self.rasters[0].width
        
        # In the case of a stack with hundreds or thousands of images, this could take a while.
        if build_arr:
            self.arr = np.array([x.arr for x in self.rasters])
        else:
            self.arr = None

    def reduce(self, fun, axis=0, name='reduced_raster'):
        """
        :param fun: A numpy function to apply to the stack of rasters (e.g. np.mean)
        :param axis: The axis to apply the function across. In most cases should be zero.
        """
        arr = self.arr if self.arr is not None else np.array([x.arr for x in self.rasters])
        tmp = fun(arr, axis=axis)
        return Raster(
            tmp, name=name, crs=self.crs, driver=self.driver, dtype=self.dtype,
            nodata=self.nodata, transform=self.transform
        )
    
    def __len__(self):
        return len(self.rasters)

    def __getitem__(self, idx):
        return self.rasters[idx]