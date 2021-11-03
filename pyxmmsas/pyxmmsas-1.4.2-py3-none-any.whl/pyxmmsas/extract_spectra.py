#/usr/bin/env python

import numpy as np
import os, sys

if len(sys.argv) <3 :
    print("Usage is %s edges.txt instrument (pn,m1,m2,pn_tim,m1_tim,me_tim) bin_n" % sys.argv[0])
    sys.exit(1)

input_times = np.loadtxt(sys.argv[1])
time0 = input_times[0]
edges = input_times[1:]

instrument = sys.argv[2]
bin_num = int(sys.argv[3])

#For development
lib_path = os.path.abspath("/home/users/f/ferrigno/Soft/pysas")
if lib_path not in sys.path:
    sys.path.append(lib_path)
else:
    print("Not appending")

import pyxmmsas
dir(pyxmmsas)

if instrument == 'pn_tim':
    my_sas = pyxmmsas.epicpn_timing('.')

if instrument == 'm1_tim':
    mos1 = pyxmmsas.epicmos_timing(1,'.')

if instrument == 'm2_tim':
    mos2 = pyxmmsas.epicmos_timing(2,'.')

#mos1.filter_withPN()
#mos2.filter_withPN()


#for i in range(1, len(edges)-1):

i = bin_num

pn_image_name = 'PNimage_%03d.fits' % i
pn_expo_map_name = 'none'
mos1_image_names = ['MOS1image_%03d.fits' % i, 'MOS1image_%03d_Timing.fits' % i]
mos2_image_names = ['MOS2image_%03d.fits' % i, 'MOS2image_%03d_Timing.fits' % i]

if instrument == 'pn_tim':
    my_sas.sas_extract_image(pn_image_name, 1000, 9000, edges[i]+time0, edges[i+1]+time0,
                            expo_map_name=pn_expo_map_name)

    pn_sas_source_coord, pn_sas_back_coord=my_sas.sas_get_extraction_region(make_plots=True,
                                                                            input_image=pn_image_name)

    my_sas.sas_extract_spectrum( pn_sas_source_coord, pn_sas_back_coord, 'spectrum_%03d'%i, edges[i]+time0,
                                 edges[i+1]+time0, run_rmf=True)

if instrument == 'm1_tim':
    mos1.sas_extract_image(mos1_image_names[0], 1000, 9000, edges[i]+time0,edges[i+1]+time0)
    mos1_source_coord, mos1_back_coord = mos1.sas_get_extraction_region(input_images=mos1_image_names,
                                                                        criterion='80',
                                                                        relative_x_offset=-3,
                                                                        rawx_low=320, rawx_high=326,
                                         make_plots=True)

    mos1.sas_extract_spectrum(mos1_source_coord, mos1_back_coord, 'spectrum_%03d' % i,
                             edges[i]+time0, edges[i+1]+time0, run_rmf=True)

if instrument == 'm2_tim':
    mos2.sas_extract_image(mos2_image_names[0], 1000, 9000, edges[i]+time0, edges[i+1]+time0,
                          time_binning=np.max([1, int((edges[i+1]-edges[i])/500)]))

    mos2_source_coord, mos2_back_coord = mos2.sas_get_extraction_region(criterion='80', make_plots=True,
                                                                      relative_x_offset=0,
                                                                      input_images=mos2_image_names )
    mos2.sas_extract_spectrum(mos2_source_coord, mos2_back_coord, 'spectrum_%03d'%i,
                              edges[i]+time0, edges[i+1]+time0, run_rmf=True)

