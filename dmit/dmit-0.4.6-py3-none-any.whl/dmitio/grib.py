#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 \nUtility to read grib data
"""
import sys
import argparse
import eccodes as ec
import pygrib
import xarray as xr
import numpy as np
import datetime as dt

class readgrib:

    def __init__(self, args:argparse.Namespace, files_to_read:list) -> None:
        if args.verbose:
            print("Reading GRIB", flush=True)
        
        self.data = self.read(args, files_to_read)

        return


    def read(self, args:argparse.Namespace, files_to_read:list) -> None:

        grid_idx = 0 # Set to 0
        lats, lons = self.get_latlons(files_to_read[grid_idx])

        Nt = len(files_to_read)
        Nt_coords = np.zeros(Nt, dtype=dt.datetime)

        found_t_2_heightAboveGround_103  = False
        found_tp_0_heightAboveGround_103 = False

        for k,f in enumerate(files_to_read):
            gids = self.get_gids(f)

            time_gid = gids[0]

            ec.codes_set(time_gid, 'stepUnits', 'm')

            date = ec.codes_get(time_gid, 'dataDate')
            time = ec.codes_get(time_gid, 'dataTime')
            lead = ec.codes_get(time_gid, 'step')

            analysis = dt.datetime.strptime(('%i-%.2i')%(date,time),'%Y%m%d-%H%M')
            forecast = analysis + dt.timedelta(minutes=lead)
            Nt_coords[k] = forecast

            for i, gid in enumerate(gids):
                shortName = ec.codes_get(gid, 'shortName')
                level = ec.codes_get(gid, 'level')
                typeOfLevel = ec.codes_get(gid, 'typeOfLevel')
                levelType = ec.codes_get(gid, 'levelType')

                Ni = ec.codes_get(gid, 'Ni')
                Nj = ec.codes_get(gid, 'Nj')

                if args.verbose:
                    print(shortName,level,typeOfLevel,levelType, flush=True)

                if (shortName=='t' or shortName=='2t') and level==2 and \
                                        typeOfLevel=='heightAboveGround' and levelType=='103':
                    values = ec.codes_get_values(gid)
                    if not found_t_2_heightAboveGround_103: t2m = np.full([Nt,lats.shape[0],lons.shape[1]], np.nan)
                    found_t_2_heightAboveGround_103 = True
                    t2m[k,:,:] = values.reshape(Nj, Ni)
                
                if (shortName=='tp' or shortName=='tprate') and level==0 and \
                                        typeOfLevel=='heightAboveGround' and levelType=='103':
                    values = ec.codes_get_values(gid)
                    if not found_tp_0_heightAboveGround_103: precip = np.full([Nt,lats.shape[0],lons.shape[1]], np.nan)
                    found_tp_0_heightAboveGround_103 = True
                    precip[k,:,:] = values.reshape(Nj, Ni)

                ec.codes_release(gid)

        ds_grib = xr.Dataset(coords={"lat": (["x","y"], lats), 
                                     "lon": (["x","y"], lons), 
                                     "time": (["t"], Nt_coords)})

        if found_t_2_heightAboveGround_103: ds_grib['t2m'] = (['time', 'lat', 'lon'], t2m - 273.15 )
        if found_tp_0_heightAboveGround_103: ds_grib['precip'] = (['time', 'lat', 'lon'], precip )

        if len(list(ds_grib.data_vars)) == 0:
            raise SystemExit('No variables found. This can be due to missing tables in ECCODES_DEFINITION_PATH or that the requested keys are not yet implemented')
 
        ds_grib = self.sort_by_time(ds_grib)

        if found_tp_0_heightAboveGround_103:
            precip_accumulated = self.is_precip_accumulated(ds_grib['precip'])
            if precip_accumulated:
                ds_grib['precip'] = self.convert_accumulated_to_rate(ds_grib['precip'])

        return ds_grib


    def is_precip_accumulated(self, precip:xr.DataArray) -> bool:
        Nt = precip.shape[0]

        precip_accumulated = True

        psum = 0
        for k in range(Nt):
            csum = np.nansum(precip[k,:,:])
            if csum < psum: # If sum decreases precip can not be accumulated
                precip_accumulated = False
            psum = csum

        return precip_accumulated


    def convert_accumulated_to_rate(self, dataarray:xr.DataArray) -> xr.DataArray:

        Nt = dataarray.shape[0]
        converted_array = dataarray.copy(deep=True)

        for k in range(1,Nt):
            converted_array[k,:,:] = dataarray[k,:,:] - dataarray[k-1,:,:]

        return converted_array


    def sort_by_time(self, dataarray:xr.Dataset) -> xr.Dataset:

        nt = dataarray.dims['time']
        parameters = list(dataarray.data_vars)

        time = dataarray['time'].values
        idx = np.argsort(time)

        da = dataarray.sortby('time')

        for p in parameters:
            for k in range(nt):
                da[p][k,:,:] = dataarray[p][idx[k],:,:]
        
        return da


    def get_latlons(self, gribfile:str) -> tuple:
        """Get latitudes and longitudes from file. Uses pygrib as eccodes have no easy interface for that.

        Parameters
        ----------
        gribfile : str
            Path to gribfile

        Returns
        -------
        tuple
            tuple of latitudes, longitudes
        """

        gr = pygrib.open(gribfile)
        lats, lons = gr[1].latlons()
        gr.close()

        return lats, lons


    def get_gids(self, gribfile:str) -> list:
        """Get GribIDs (gid) for all the messages in one gribfile

        Parameters
        ----------
        gribfile : str
            path to gribfile

        Returns
        -------
        list
            list of grib-ids
        """
        
        f = open(gribfile, 'rb')
        msg_count = ec.codes_count_in_file(f)
        gids = [ec.codes_grib_new_from_file(f) for i in range(msg_count)]
        f.close()

        return gids

    # def find_keys(self, args:argparse.Namespace) -> None:
    #     return


# ---------- Kept only for backward compability ----------- #
class grib_reader:
    """Class to read and get data from gribfile
    DEPRECATED
    """

    def __init__(self, namelist):
        """Init for grib_reader

        Parameters
        ----------
        namelist : dict
            dictionary containing namelist
        """
        variables = [k for k in namelist['grib_translators'].keys()]

        self.search_t2m = True if "t2m" in variables else False
        self.search_tp  = True if "precip" in variables else False

        self.found_t2m = False
        self.found_tp = False
        
        return


    def get_latlons(self, gribfile):
        """Uses pygrib to get coordinates
        Parameters
        ----------
        gribfile : str
            path to gribfile

        Returns
        -------
        array
            array with latitudes
        array
            array with longitudes
        """
        gr = pygrib.open(gribfile)
        lats, lons = gr[1].latlons()
        gr.close()
        return lats, lons


    def get_data(self, gribfiles, namelist, stepunit="m"):
        """Get data from gribfiles according to a namelist

        Parameters
        ----------
        gribfiles : list
            list with paths to gribfiles
        namelist : dict
            namelist of job

        Returns
        -------
        xarray.Dataset
            Dataset with data from gribfile
        """

        gribfiles = list(gribfiles)

        lats, lons = self.get_latlons(gribfiles[0])

        Nt = len(gribfiles)
        time = np.empty(Nt, dtype='i8')

        init = True
        k=0
        for gribfile in gribfiles:

            f = open(gribfile, 'rb')

            while True:

                gid = ec.codes_grib_new_from_file(f)
                if gid is None:
                    break

                ec.codes_set(gid, 'stepUnits', stepunit)

                if init:
                    latdim = ec.codes_get(gid, 'Ny')
                    londim = ec.codes_get(gid, 'Nx')
                    if self.search_t2m: t2m = np.zeros([Nt,latdim,londim])
                    if self.search_tp: tp = np.zeros([Nt,latdim,londim])
                    init=False

                shortName = ec.codes_get(gid, 'shortName')
                level = ec.codes_get(gid, 'level')
                dataDate = ec.codes_get(gid, 'dataDate')
                dataTime = ec.codes_get(gid, 'dataTime')
                leadTime = ec.codes_get(gid, 'step')

                
                ct = dt.datetime.strptime('{}{:02d}'.format(dataDate,dataTime), '%Y%m%d%H%M') + dt.timedelta(minutes=leadTime)
                time[k] = int((ct - dt.datetime(1970,1,1,0)).total_seconds())

                if (self.search_t2m) and (shortName=='t') and (level==2):
                    values = ec.codes_get_values(gid)
                    t2m[k,:,:] = values.reshape((latdim,londim))
                    self.found_t2m = True
                if (self.search_tp) and (shortName=='tp') and (level==0):
                    values = ec.codes_get_values(gid)
                    tp[k,:,:] = values.reshape((latdim,londim))
                    self.found_tp = True
                
                    
                ec.codes_release(gid)

            f.close()
            k+=1


        ds = xr.Dataset(
            data_vars=dict(
            ),
                coords=dict(
                    lon=(["y", "x"], lons),
                    lat=(["y", "x"], lats),
                    time=time,
                    )
            )

        if self.found_t2m: 
            t2m[np.where(t2m==0)] = np.nan
            ds = ds.assign(t2m= (("time", "y", "x"), t2m))
        if self.found_tp: 
            ds = ds.assign(tp= (("time", "y", "x"), tp))

        ds.attrs['starttime'] = time[0]
        
        return ds


