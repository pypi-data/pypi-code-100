import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from numpy import ndarray

from aislab.op_nlopt.ord12 import *
from aislab.op_nlopt.cstm import *
from aislab.gnrl.sf import *
from aislab.gnrl.measr import *

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

mdl_types = ['exp2', 'log1', 'exp', 'log', 'lgr', 'lin']
mdl_types = ['exp', 'log', 'lgr', 'lin']
mdl_types = ['log2']
mdl_types = ['exp2', 'log2', 'lin', 'lgr']
mdl_types = ['lgr']
for mdl_type in mdl_types:

    item = 'AA0878'
    data = pd.DataFrame({'x' : [-0.0, 24.675324675324674, 35.064935064935064], 'y' : [1, 1.2608695652173914, 1.45], 'w' : [0.31, 0.35, 0.35]}); item = 'AA0878'
    # item = 'AA2257'
    # data = pd.DataFrame({'x' : [-0.0, 27.272727272727273, 45.45454545454545, 50.0, 54.54545454545455], 'y' : [1, 1.1666666666666667, 1.0, 1.0, 1.1538461538461535], 'w' : [0.15, 0.18, 0.1, 0.2, 0.38]}); item = 'AA2257'
    # item =    'AA2297'
    # data = pd.DataFrame({'x' : [-0.0, 5.2631578947368425], 'y' : [1, 1.1666666666666667], 'w' : [0.48, 0.52]}); item = 'AA2297'
    # item =    'AA2291'
    # data = pd.DataFrame({'x': [-0.0, 46.153846153846146, 61.53846153846154, 69.23076923076923], 'y': [1, 1.1162790697674418, 1.175, 1.1395348837209305], 'w': [0.06, 0.31, 0.31, 0.32]});
    # item = 'XXX'
    # data = pd.DataFrame({'x': [30. , 27.5, 25. , 22.5, 20. , 17.5, 10. , -0. ], 'y': [6.70912296, 1.40873016, 6.35330056, 5.65689653, 6.23105281, 6.88002254, 2.08811946, 1.], 'w': [100000., 0., 0.26, 0., 0.09, 0., 0., 0.56]})
    # item = 'XXX'
    # data = pd.DataFrame({'x': [0, 0.05, 0.10, 0.15, 0.20, 0.25 ], 'y': [1, 1.5, 2, 5, 10, 20], 'w': [100, 1, 2, 3, 4, 5]})
    # x = np.array([0, 5, 10, 15, 20, 25]); y = exp3_apl(x, [0.9, 0.1, 0.2])
    # data = pd.DataFrame({'x': x, 'y': y, 'w': [100, 1, 2, 3, 4, 5]})

    xx = np.arange(0, np.max(data['x']) + 0.05, 0.05)

    # OVERWRITE
    data['w'] = 1
    x = c_(data.loc[:, 'x'].values); #    x = x[::-1]
    y = c_(data.loc[:, 'y'].values)
    w = c_(data.loc[:, 'w'].values)
    if len(x.shape) == 1: x = c_(x)
    N = len(w)
    max_lgr = 0.9 # goto config
    if mdl_type == 'lgr': y, st = rnml(y, 0, max_lgr)
    ####################################################
    cnames = 'x'
    metpminit = 'zero' # 'fapp' #
    gcnv = 1e-3
    ####################################################
    # Initial model parameters
    if mdl_type == 'lgr':
        Nw = sum(w)
        my = y.T@w/Nw
        lambda_ = np.log(my/(1 - my))
        if metpminit == 'zero':     pm0 = np.vstack((c_([lambda_]), [0]))
        elif metpminit == 'fapp':   pm0 = lspm(x, (y - 0.5)*2*lambda_)
    elif mdl_type == 'exp':
        pm0 = np.array([y.mean() - 1, 1/np.mean(np.exp(x))]).reshape(2,1)
    elif mdl_type == 'exp2':
        # c = 0.1;
        # xmax, ind = max1(x.flatten())
        # ymax = y[ind, 0]
        # b = np.max([np.min([ymax - 1, 100]), 0])/(np.exp(c*xmax) - 1)
        # ind = x != 0
        # xc = np.mean(x[ind])
        # yc = np.mean(y[ind])
        # b = np.max([np.min([yc - 1, 100]), 0])/(np.exp(c*xc) - 1)
        # a = 1 - b
        # pm0 = c_(np.array([a, b, c]))
        ind = x != 0
        xc = np.mean(x[ind])
        yc = np.mean(y[ind])
        c = np.log(2*yc - 1)/xc
        b = np.max([np.min([yc - 1, 100]), 0])/(np.exp(c*xc) - 1)
        a = 1 - b
        pm0 = c_(np.array([a, b, c]))

    elif mdl_type == 'log':
        pm0 = np.array([y.mean() - 1, 1/np.mean(np.log(abs(x)+1))]).reshape(2,1)
    elif mdl_type == 'log2':
        # c = 0.1
        # xmax = np.max(x)
        # ymax = np.max(y)
        # b = np.max([np.min([ymax - 1, 100]), 0])/(np.log(abs(c*xmax + 1)))
        # a = b - 1
        # pm0 = c_(np.array([a, b, 5*c]))
        c = 10
        xmax = np.max(x)
        ymax = np.max(y)
        b = np.max([np.min([ymax - 1, 100]), 0])/(np.log(abs(c*xmax + 1)))
        a = b - 1
        pm0 = c_(np.array([a, b, 5*c]))

    # Arguments for func, grad, hes calculation
    args = {}
    args['data'] = np.hstack((x, y, w, np.zeros((N, 1))))
    args['cnames'] = c_(['a', 'b'])
    args['x'] = pm0
    args['ivi'] = 0
    args['pm0'] = pm0
    args['metpminit'] = metpminit
    args['b'] = 1e-8 # 1e-2
    args['c'] = 1e3

    #    func = par['func
    #    grad = par['grad
    #    hes = par['hes
    if mdl_type == 'lgr' or mdl_type == 'lin':
        pass
        N = len(w)
        x = np.hstack((ones((N, 1)), x))
        args['data'] = np.hstack((x, y, w, np.zeros((N, 1))))

    if mdl_type != 'lin':
        if mdl_type == 'exp2':   pm, F, g, H, Hinv, __ = newton(pm0, f_exp3, g_exp3, h_exp3, args, gcnv, maxiter=1000, rcondH=0, dsp_op=2, s=0.1)
        elif mdl_type == 'lgr1': pm, F, g, H, Hinv, __ = newton(pm0, f_lgr1, g_lgr1, h_lgr1, args, gcnv, rcondH=0, dsp_op=2)
        elif mdl_type == 'exp':  pm, F, g, H, Hinv, __ = newton(pm0, f_exp1, g_exp1, h_exp1, args, gcnv, rcondH=0, dsp_op=2)
        elif mdl_type == 'lgr': pm, F, g, H, Hinv, __ = newton(pm0, f_lgr, g_lgr, h_lgr, args, gcnv, rcondH=0, dsp_op=2)
        elif mdl_type == 'log': pm, F, g, H, Hinv, __ = newton(pm0, f_log1, g_log1, h_log1, args, gcnv, rcondH=0, dsp_op=2)
        elif mdl_type == 'log2': pm, F, g, H, Hinv, __ = newton(pm0, f_log3, g_log3, h_log3, args, gcnv, maxiter=1000, rcondH=0, dsp_op=2)
    else:
        pm = lspm(x, y)

    if not mdl_type == 'lgr': pm[pm < 0] = 0


    if mdl_type == 'exp':
        ym = exp_apl(x, pm)
        print('VAF_exp = ', vaf(y, ym), ',   pm =', pm.flatten())
    if mdl_type == 'exp2':
        ym = exp3_apl(x, pm)
        print('VAF_exp2 = ', vaf(y, ym), ',   pm =', pm.flatten())
    elif mdl_type == 'lgr':
        ym = lgr_apl(x, pm)
        print('VAF_lgr = ', vaf(y, ym), ',   pm =', pm.flatten())
    elif mdl_type == 'log':
        ym = log_apl(x, pm)
        print('VAF_log = ', vaf(y, ym), ',   pm =', pm.flatten())
    elif mdl_type == 'log2':
        ym = log3_apl(x, pm)
        print('VAF_log = ', vaf(y, ym), ',   pm =', pm.flatten())
    elif mdl_type == 'lin':
        ym = lspm_apl(x, y, mdl)
        print('VAF_lin = ', vaf(y, ym), ',   pm =', pm.flatten())
    if np.shape(x)[1] > 1: x = c_(x[:,1])
    #xx: ndarray = np.array(range(0, max([25, int(np.ceil(x.max()))+1]) ))

    plt.scatter(x, y)
    plt.plot(x, ym, 'r')
    plt.show()


    if mdl_type == 'exp':   ym = exp_apl(xx, pm)
    elif mdl_type == 'exp2': N = len(xx); ym = exp3_apl(xx, pm)
    elif mdl_type == 'lgr':
        N = len(xx); xx = np.hstack((ones((N, 1)), c_(xx))); ym = lgr_apl(xx, pm)
    elif mdl_type == 'log': ym = log_apl(xx, pm)
    elif mdl_type == 'lin': N = len(xx); xx = np.hstack((ones((N, 1)), c_(xx))); ym = lspm_apl(xx, y, mdl); xx = xx[:,1]
    elif mdl_type == 'log2': N = len(xx); ym = log3_apl(xx, pm);

    if mdl_type == 'lgr':
        y, st = rnml(y, st['minx'], st['maxx'])
        ym, st = rnml(ym, st['minx'], st['maxx'])

    plt.plot(xx[:,1], ym, 'r')
    plt.title(item)
    plt.show()
    1;
    #
    # import matplotlib.pyplot as plt
    # plt.plot(y)
    # plt.plot(ym)
    # plt.show
    #
    # # print('Optimal params:')
    # # print(pm)
ym = exp3_apl(x, pm0)
print('VAF_exp2(pm0) = ', vaf(y, ym), ',   pm0 =', pm.flatten())
ym = exp3_apl(x, pm)
print('VAF_exp2(pm) = ', vaf(y, ym), ',   pm =', pm.flatten())
