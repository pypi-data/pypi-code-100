#!/usr/bin/env python
#---------------------------------------------------------------------------
# Copyright 2021 Takafumi Ogawa
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#---------------------------------------------------------------------------
# pydecs-main module
# pydecs = PYthon code for Defect Equilibria in Crystalline Solids
# Library-homepage = /https://gitlab.com/tkog/pydecs
# Citation: ***
#---------------------------------------------------------------------------
import os,sys
import numpy as np
import shutil
import time

from pydecs.inout  import InputParamsToml
from pydecs.eqcond import EquilibriumConditions
from pydecs.solver import DefectEqSolver
from pydecs.inout  import output_density_with_eqcond
from pydecs.inout  import plot_defect_densities

def pydecs_main():
    print(f"-"*100)
    print(f" Starting pydecs (PYthon code for Defect Equilibria in Crystalline Solids)")
    fnin_toml="inpydecs.toml"
    if len(sys.argv)>1:
        fnin_toml=sys.argv[1]
    print(f" Input toml-file = {fnin_toml}")
    print(f"-"*100)
    if not os.path.exists(fnin_toml):
        print(f" ERROR:: file not-found: {fnin_toml}")
        print(f"-"*100)
        sys.exit()
    intoml=InputParamsToml(fnin_toml)
    inparams=intoml.get_input_parameters()
    root_outfiles=intoml.get_root_outfiles()
    dirname=f"{root_outfiles}_outdata"
    if os.path.exists(dirname):
        shutil.rmtree(dirname)
        time.sleep(0.01)
    os.makedirs(dirname)
    time.sleep(0.01)
    os.chdir(dirname)
    input_paths=[]
    for p1 in intoml.get_input_paths():
        input_paths.append(f"../{p1}")
    eqcond1=EquilibriumConditions(inparams["eq"],input_paths,root_outfiles)
    elements=eqcond1.get_elements()
    solver1=DefectEqSolver(inparams["host"],elements,input_paths)
    fnout_dens_csv=root_outfiles+"_densities.csv"
    for ieq1,eqc1 in enumerate(eqcond1):
        ieq2_str=f"{ieq1+1:0>4}"
        dirname=f"cond{ieq2_str}"
        print(f"Eq-condition-loop ({ieq1+1}) starting at {dirname}")
        os.makedirs(dirname,exist_ok=True)
        os.chdir(dirname)
        defect_densities=solver1.opt_coordinator(eqc1,inparams["solver"],root_outfiles,inparams["plot"])
        os.chdir("../")
        if not isinstance(defect_densities,str):
            defect_densities[0][-1]=ieq1+1
            output_density_with_eqcond(defect_densities,eqc1,fnout_dens_csv)
        print("*"*100)
    if not isinstance(defect_densities,str):
        inparams["plot"]["outfiles_header"]=root_outfiles
        inparams["plot"]["input_filename"]=fnout_dens_csv
        plot_defect_densities(inparams["plot"])
    print("*"*100)
    print(f" Finished!")
    print("*"*100)


if __name__=="__main__":
    pydecs_main()
