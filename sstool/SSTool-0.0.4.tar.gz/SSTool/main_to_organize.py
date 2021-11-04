import numpy as np
import pandas as pd
import sympy as sym
import matplotlib.pyplot as plt
from control.matlab import *
# from Functions_v1 import *
# from core.functions_to_organize import *
# from core import functions_to_organize
from engine import build

# core
# RLs, Cs, VSCs, Isum, Xdivs, SGs, data = CSystem('datafiles/annakkage_luis_v5.xlsx')
# RLs, Cs, VSCs, Isum, Xdivs, SGs, data = functions_to_organize.CSystem('datafiles/annakkage_luis_v5.xlsx')

x = build.create_syst(1)
print(x)






# nyquist:
# merge_all_minus1('Datafiles/annakkage_luis_v5.xlsx', RLs, Cs, VSCs, Isum, Xdivs)  # good, for python
# check_nyq_py_mt('Datafiles/Matlab_check/eig_out.csv', 'Datafiles/annakkage_luis_v5.xlsx', RLs, Cs, VSCs, Isum, Xdivs)  # python and matlab matching the nyquist


# stability analysis
# Stability_Analysis.bode_YZ(ss_class=VSCs[0], f_ini=0, f_fin=2, name_in=['vq_1', 'vd_1'], name_out=['iqxv_1', 'idxv_1'], n_p=1000, logx=False, dBy=False, invert=False)
# Stability_Analysis.eigenval_YZ(ss_class=VSCs[0], f_ini=0, f_fin=2.85, name_in=['vq_1', 'vd_1'], name_out=['iqxv_1', 'idxv_1'], n_p=1000, invert=False)
# Stability_Analysis.eigen(VSCs[0], plot=False, prnt=True)  # can also pass VSCs[0]
# Stability_Analysis.nyquist_YZ(ss_class=VSCs[0], f_ini=0, f_fin=5, name_in=['vq_1', 'vd_1'], name_out=['iqxv_1', 'idxv_1'], n_p=10000, n_arrows=5, invert=False)


# check with matlab
# check_eigen_py_mt('Datafiles/Matlab_check/vsc_eigen1.csv', ss_class=VSCs[0], f_ini=0, f_fin=2.85, name_in=['vq_1', 'vd_1'], name_out=['iqxv_1', 'idxv_1'], n_p=1000, invert=False)

# analyze matlab results
# bode_2x2(ss_class=mtlb, f_ini=0, f_fin=2, name_in=['NET.v1_q', 'NET.v1_d'], name_out=['NET.i1_q', 'NET.i1_d'], n_p=1000, logx=False, dBy=False, invert=False)
# eigen(mtlb, plot=True, prnt=False)

# analyze comparison
# bode_compare(ss_class_py=VSCs[0], ss_class_mt=mtlb, f_ini=0, f_fin=2, name_in_py=['vq_1', 'vd_1'], name_out_py=['iqxv_1', 'idxv_1'], name_in_mt=['NET.v1_q', 'NET.v1_d'], name_out_mt=['NET.i1_q', 'NET.i1_d'], n_p=1000)


