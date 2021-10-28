# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 15:22:41 2021

@author: chris.kerklaan
"""
import importlib
from pathlib import Path


HAS_THREEDIDEPTH = importlib.util.find_spec("threedidepth")

if HAS_THREEDIDEPTH:
    from threedidepth.calculate import calculate_waterdepth

    class ThreediDepth:
        def __init__(self, folder, dem_path):
            self.folder = folder
            self.nc_path = self.folder + "/results_3di.nc"
            self.ga_path = self.folder + "/gridadmin.h5"
            self.dem_path = dem_path
            self.folder_name = Path(self.folder).stem

        def calculate(self, calculation_steps=[-1]):
            for calculation_step in calculation_steps:
                name = self.folder + f"/{self.folder_name}_depth_{calculation_step}.tif"
                calculate_waterdepth(
                    self.ga_path,
                    self.nc_path,
                    self.dem_path,
                    name,
                    calculation_steps=[int(calculation_step)],
                )
