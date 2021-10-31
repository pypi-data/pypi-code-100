# S T E P W I S E   L I N E A R  R E G R E S S I O N
#--------------------------------------
# Author: Alexander Efremov
# Date:   05.09.2009 /matlab version/
# Course: Multivariable Control Systems
#--------------------------------------
import numpy as np
import pandas as pd
import copy
from numpy.matlib import repmat
from gnrl.sf import *
from gnrl.measr import *

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('precision', 5)

# def gswlinr():
###################################################################################
###################################################################################
def bElimin(model, st0, met, cnames, s_min, SLS, crit_nbm, iterate):
    Nw, z, FY, FF, wF, ivi, ivo, n1, n2 = parin(st0, model[-1])
    # ----- Calculate significance of factors in the model -----
    if met == 'FR' and n2 == z:
        iterate = 0
        return model, iterate
    ivi0 = ivi
    ivo0 = ivo
    if ivi.shape[0] > 1:
        n1 = ivi.shape[0]
        n2 = n2 - 1
        pm = nans((n2, n1))
        st = []
        for i in np.arange(n1):
            ivi = ivi0[np.hstack((np.arange(0, i), np.arange(i + 1, n1)))]
            pmi, P = mdl(submat(FF, ivi, ivi), submat(FY, ivi), s_min)
            pm[:, i] = pmi[:, 0]
            st = st + [stmdl('BE', model[-1], submat(FY, ivi), P, submat(wF, ivi), n2, n1, st0)]
        st_in = [s['in'] for s in st]
        model[-1] = htmdl('BE2', model[-1], st=st_in)
        flg = 1
    else:
        # model[-1] = htmdl('BE2', model[-1])
        flg = 0
    # ----- Find next best model -----
    if met == 'FR': return model, st0, iterate
    if flg:
        p_Fpi, pmi, sti, ind = nextmdl('BE2', model, st, pm, crit_nbm)
        if p_Fpi > SLS:
            ivi = delrc(ivi0, ind)
            ivo = np.hstack((ivo, ivi0[ind]))
            z = htmdl('BE1', model[-1], 'BE', n2, ivi, ivo, cnames, ivi0[ind], pmi, sti)
            model = model + [z]
        else:
            if met == 'BR':
                iterate = 0
            else:
                model[-1]['FB'] = 'BE_stop'
    elif met == 'BR':
        iterate = 0
    else:
        model[-1]['FB'] = 'BE_stop'
    return model, iterate


###################################################################################
def firstmdl(st0, mtp, s_min, cnames, ivi):
    if mtp == 'full':
        z = st0['z']
        FF = st0['FF']
        FY = st0['FY']
        wF = st0['wF']
        ivi = np.arange(z)
        ivo = np.array([]).astype(int)
        n2 = z
        pm, P = mdl(FF, FY, s_min)
        st_ext = stmdl('BE1', [], FY, P, wF, n2, [], st0)
        # st_ext2 = stmdl('FS1', [], FY, P, wF, n2, [], st0)
        model = [htmdl('BE1', [], 'BE', n2, ivi, ivo, cnames, [], pm, st_ext['ovr'])]
    elif mtp == 'empty':
        z = st0['z']
        FF = np.array([[st0['FF'][0, 0]]])
        FY = np.array([st0['FY'][0]])
        wF = np.array([st0['wF'][0, 0]])
        ivi = np.array([0])
        ivo = np.arange(1, z)
        n2 = 1
        pm, P = mdl(FF, FY, s_min)
        st_ext = stmdl('FS1', [], FY, P, wF, n2, [], st0)
        model = [htmdl('FS1', [], 'FS', n2, ivi, ivo, cnames, [], pm, st_ext['ovr'])]
    elif mtp == 'init':
        z = st0['z']
        ivo = np.array(list(set(np.arange(z)) - set(ivi.flatten())))
        n2 = ivi.shape[0]
        FF = submat(st0['FF'], ivi, ivi)
        FY = submat(st0['FY'], ivi)
        wF = submat(st0['wF'], ivi)
        pm, P = mdl(FF, FY, s_min)
        st_ext = stmdl('FS1', [], FY, P, wF, n2, [], st0)
        model = [htmdl('FS1', [], 'FS', n2, ivi, ivo, cnames, [], pm, st_ext['ovr'])]
    else:
        raise Exception('Initial model structure is not defined...')
    return model
###################################################################################
def fSelect(model, st0, met, cnames, s_min, SLE, crit_nbm, iterate):
    # if len(model) > 1 and len(model[-1]['st']['in']) == 0: return model, st0, par # las1
    if model[-1]['FB'] == 'BE':
        if iterate == 0: iterate = -1
        return model, iterate  # las1t step was BE

    # todo: calc model(end).st.out when BR is succesfull --> calc in bElimin.m
    # if length(model) > 1 && isempty(model(end).st_in),  model_new = model(end);  model = model(1:end - 1); # successful BE step
    # else,                                               model_new = [];
    # end
    Nw, z, FY, FF, wF, ivi, ivo, n1, n2 = parin(st0, model[-1])
    # ----- Calculate significance of not entered factors  -----
    if not len(ivo) == 0:
        n1 = ivi.shape[0]
        n2 = n1 + 1
        ivi0 = np.hstack((np.matlib.repmat(ivi, z - n1, 1), c_(ivo)))
        pm = nans((n2, len(ivo)))
        st = []
        for i in np.arange(z - n2 + 1):
            ivi = ivi0[i, :]
            pmi, P = mdl(submat(FF, ivi, ivi), submat(FY, ivi), s_min)
            pm[:, i] = pmi[:, 0]
            st = st + [stmdl('FS', model[-1], submat(FY, ivi), P, submat(wF, ivi), n2, n1, st0)]
        st_out = [s['out'] for s in st]
        model[-1] = htmdl('FS2', model[-1], st=st_out)
        flg = 1
    else:
        # model[-1] = htmdl('FS2', model[-1])
        flg = 0
    # ----- Find next best model -----
    # todo: calc model(end).st_in when BR is succesfull --> calc in bElimin.m
    # if ~strcmp(met, 'FR') && ~isempty(model_new), model(end + 1) = model_new; return, end   # Successful BE step
    if flg:
        p_Fpi, pmi, sti, ind = nextmdl('FS2', model, st, pm, crit_nbm)
        if not len(p_Fpi) == 0 and p_Fpi <= SLE:
            ivi = ivi0[ind[0], :]
            ivo1 = ivo[ind[0]]
            ivo = np.delete(ivo, ind, 0)
            model = model + [htmdl('FS1', model[-1], 'FS', n2, ivi, ivo, cnames, ivo1, pmi, sti)]
        else:
            iterate = 0
    else:
        iterate = 0
    return model, iterate


###################################################################################
def htmdl(mode=None, model0=None, FB=None, n2=None, ivi=None, ivo=None, cnames=None, ind2=None, pm=None, st={}):
    model = copy.deepcopy(model0)
    if len(model) == 0: model = {}; model
    if not 'st' in model:  model['st'] = {}
    if not 'in' in model['st']:  model['st']['in'] = {}
    if not 'out' in model['st']: model['st']['out'] = {}
    if not 'ovr' in model['st']: model['st']['ovr'] = {}
    # Model history
    if mode == 'FS1' or mode == 'BE1':
        model['cname_i'] = np.array(cnames)[ivi]
        model['cname_o'] = np.array(cnames)[ivo]
        model['FB'] = FB
        model['n'] = n2
        model['xio'] = np.array(cnames)[ind2]
        model['pm'] = pm
        model['ivi'] = ivi
        model['ivo'] = ivo
        model['st']['in'] = {}
        model['st']['out'] = {}
        model['st']['ovr'] = st
    elif mode == 'FS2':
        model['st']['out'] = st
    elif mode == 'BE2':
        model['st']['in'] = st
    return model


###################################################################################
def mdl(FF=None, Fy=None, s_min=None):
    if FF.size == 1:
        P = 1/FF
    else:
        rcM = 1/np.linalg.cond(FF)  # todo: create function in sf, calculating condition number
        if rcM < 1e-3:
            P = nsinv(FF, s_min)
        else:
            P = np.linalg.inv(FF)
        # P = nsinv(FF, s_min)
    pm = P@Fy
    return pm, P


###################################################################################
def nextmdl(mode=None, model=None, st_ovr=None, pm=None, crit=None):
    if len(model) > 1:
        model1 = model[-2]
    else:
        model1 = None
    model = model[-1]
    if mode == 'FS2':
        st = model['st']['out']
        n = len(st)
        Fp = nans((n, 1))
        for i in np.arange(n): Fp[i] = st[i]['Fp']
        p_Fp = nans((n, 1))
        for i in np.arange(n): p_Fp[i] = st[i]['p_Fp']
        cnd = np.ones((n, 1)) == 1
        if len(crit) > 0:
            #if 'Fp4' in crit: cnd = cnd & (Fp >= 4)
            if 'AIC' in crit and model1 is not None:
                aic = nans((n, 1))
                for i in np.arange(n): aic[i] = st[i]['AIC']
                cnd1 = aic <= model1['st']['ovr']['AIC']
                cnd2 = np.isinf(aic) & (np.sign(aic) == -1)  # aic = -inf
                cnd = cnd & (cnd1 | cnd2)
            if 'Cp' in crit and model1 is not None:
                cp = nans((n, 1))
                for i in np.arange(n): cp[i] = st[i]['Cp']
                cnd1 = (cp > model1['n'] - 1) | (cp < 0)
                cnd2 = np.isnan(cp)
                cnd = cnd & (cnd1 | cnd2)
        __, ind1 = sort(Fp, 'descend')
        ind = ind1[find(cnd[ind1.flatten()], 1, 'first')]
        if not len(ind) == 0:
            p_Fpi = p_Fp[ind]
            pmi = pm[:, ind]
            st_ovri = st_ovr[ind[0]]['ovr']
        else:
            p_Fpi = []
            pmi = []
            st_ovri = []
    else:
        if mode == 'BE2':
            n = len(model['st']['in'])
            p_Fp = nans((n, 1))
            for i in np.arange(n):
                p_Fp[i] = model['st']['in'][i]['p_Fp']
            p_Fpi, ind = max1(p_Fp, naskip=True)
            pmi = c_(pm[:, ind])
            st_ovri = st_ovr[ind]['ovr']
    return p_Fpi, pmi, st_ovri, ind


###################################################################################
def parin(st0, model):
    Nw = st0['Nw']
    z = st0['z']
    FY = st0['FY']
    FF = st0['FF']
    wF = st0['wF']
    ivi = model['ivi']
    ivo = model['ivo']
    n1 = len(ivi) - 1
    n2 = n1 + 1
    return Nw, z, FY, FF, wF, ivi, ivo, n1, n2


###################################################################################
def stats(x=None, y=None, w=None):
    N, z = x.shape
    Nw = sum(w)
    FF = x.T@(w*x)
    FY = x.T@(w*y)
    wF = w.T@x
    mF = x.T@w/Nw
    my = y.T@w/Nw
    ssy = y.T@(y*w)
    sst = (y - my).T@((y - my)*w)
    YFPFY = FY.T@nsinv(FF)@FY
    sse = np.array([np.max(np.hstack((0, (ssy - YFPFY).flatten())))])
    mset = sse/(N - z)
    st0 = {'N': N,
           'Nw': Nw,
           'z': z,
           'FF': FF,
           'FY': FY,
           'wF': wF,
           'mF': mF,
           'my': my,
           'ssy': ssy,
           'sst': sst,
           'mset': mset
           }
    return st0


###################################################################################
def stmdl(FB=None, model=None, FY=None, P=None, wF=None, n2=np.nan, n1=np.nan, st0=None):
    my = st0['my']
    N = st0['N']
    Nw = st0['Nw']
    ssy = st0['ssy']
    sst = st0['sst']
    mset = st0['mset']
    if not len(model) == 0:
        ssm_1 = model['st']['ovr']['SSM']
        sse_1 = model['st']['ovr']['SSE']
    # else:
    #     ssm_1 = np.nan
    #     sse_1 = np.nan
    YFPFY = FY.T@P@FY
    sse = np.array([np.max(np.hstack((0, (ssy - YFPFY).flatten())))]) # matlab syntaxis: sse = max([0, ssy - YFPFY])
    ssm = np.array([np.max(np.hstack((0, YFPFY.flatten())))])
    ssr = np.array([np.max(np.hstack((0, (YFPFY + Nw*my**2 - 2*my*wF@P@FY).flatten())))])
    v1o = n2
    v2 = N - n2
    Fo = ssr/sse*v2/v1o
    p_Fo = pvalF(Fo, v1o, v2, 'ot')
    mse = sse/(N - n2)
    ste = c_(np.sqrt(np.diag(P)*mse).flatten())
    R2 = ssr/sst
    R2adj = 1 - (1 - R2)*(Nw - 1)/(Nw - n2)
    vaf = np.array([np.max(np.hstack((0, R2adj.flatten())))])*100
    cp = sse/mset + 2*n2 - N
    aic = np.log(sse) + 2/N*n2
    sc = np.log(sse) + np.log(N)/N*n2
    if not len(model) == 0 and 'ovr' in model['st'] and 'R2' in model['st']['ovr']:
        R2_1 = model['st']['ovr']['R2']
    # else:
    #     R2_1 = np.nan
    if FB == 'FS':
        R2prt = R2 - R2_1
        v1p = np.abs(n2 - n1)
        t2ss = np.array([np.max(np.hstack((0, (ssm - ssm_1).flatten())))])
        Fp = t2ss/sse*v2/v1p
        p_Fp = pvalF(Fp, v1p, v2, 'ot')
    elif FB == 'BE':
        R2prt = R2_1 - R2
        v1p = np.abs(n2 - n1)
        t2ss = np.array([np.max(np.hstack((0, (ssm_1 - ssm).flatten())))])
        Fp = t2ss/sse_1*v2/v1p
        p_Fp = pvalF(Fp, v1p, v2, 'ot')
    else:
        R2prt = None
        v1p = None
        t2ss = None
        Fp = None
        p_Fp = None

    st = {};
    st['ovr'] = {}
    st['ovr']['v1'] = n2
    st['ovr']['v2'] = v2
    st['ovr']['SSR'] = ssr
    st['ovr']['SSM'] = ssm
    st['ovr']['SSE'] = sse
    st['ovr']['MSE'] = mse
    st['ovr']['STE'] = ste
    st['ovr']['R2'] = R2
    st['ovr']['R2adj'] = R2adj
    st['ovr']['VAF'] = vaf
    st['ovr']['BIC'] = sc
    st['ovr']['Fo'] = Fo
    st['ovr']['p_Fo'] = p_Fo
    st['ovr']['Cp'] = cp
    st['ovr']['AIC'] = aic

    if FB == 'FS':
        st['out'] = {}
        st['out']['v1p'] = v1p
        st['out']['t2ss'] = t2ss
        st['out']['Fp'] = Fp
        st['out']['p_Fp'] = p_Fp
        st['out']['R2prt'] = R2prt
        st['out']['Cp'] = cp
        st['out']['AIC'] = aic
    elif FB == 'BE':
        st['in'] = {}
        st['in']['t2ss'] = t2ss
        st['in']['Fp'] = Fp
        st['in']['p_Fp'] = p_Fp
        st['in']['v1p'] = v1p
        st['in']['R2prt'] = R2prt
        st['in']['Cp'] = cp
        st['in']['AIC'] = aic
    return st


###################################################################################
def swlinr(x=None, y=None, w=None, cnames=None, pm0=1, met='SWR', SLE=0.05, SLS=0.05, crit_nbm=['Cp', 'AIC'], mtp='empty', ivi=np.empty([1,]).astype(int), val_prc=0, s_min=1e-12, dsp='all'):
    N = x.shape[0]
    if cnames is None: cnames = ['var_' + str(i) for i in range(m)]
    if pm0 == 1:
        x = np.hstack((np.ones((N, 1)), x))
        cnames = ['intercept'] + cnames
        ivi = np.hstack((1, ivi + 1))
    st0 = stats(x, y, w)
    model = firstmdl(st0, mtp, s_min, cnames, ivi)
    iterate = 1
    while iterate > 0:
        model, iterate = bElimin(model, st0, met, cnames, s_min, SLS, crit_nbm, iterate)
        model, iterate = fSelect(model, st0, met, cnames, s_min, SLE, crit_nbm, iterate)
        visualz(model, iterate, dsp, mtp)
    return model


###################################################################################
def visualz(model, iterate, dsp, mtp):
    if dsp == 'no': return
    model0 = copy.deepcopy(model)
    i2 = iterate
    if i2 == -1:
        i1, i2 = 1, 0
    else:
        i1 = 0
    for step in np.arange(len(model0) - 2 + i1, len(model0) - i2):
        model = model0[step]
        print('Step: ', step, '  =================================================================================================================')
        if model['FB'] == 'FS' and step != 0:
            print('Added factor: ', model['xio'])
        elif model['FB'] == 'BE' and step != 0:
            print('Removed factor: ', model['xio'])
        elif mtp == 'init':
            print('Initial model: ', model['cname_i'].flatten())
        elif model['FB'] == 'FS' and step == 0:
            print('Initial model: intercept')
        elif model['FB'] == 'BE' and step == 0:
            print('Initial model: full')
        elif model['FB'] == 'BE' and step == 0:
            print('Initial model: full')

        if 'Fo' in model['st']['ovr'] and dsp == 'all' or dsp == 'ovr':
            print('--- Overall model measures ---')
            st = model['st']['ovr']
            df1 = np.full((1, 1), st['v1'])
            df2 = np.full((1, 1), st['v2'])
            #    SSR = st['SSR']
            #    SSM = st['SSM']
            SSE = st['SSE']
            MSE = st['MSE']
            R2 = st['R2']
            R2a = st['R2adj']
            VAF = st['VAF']
            BIC = st['BIC']
            AIC = st['AIC']
            Cp = st['Cp']
            OverallF = st['Fo']
            pval_OverallF = st['p_Fo']
            print(pd.DataFrame({'df1': df1[0],
                                'df2': df2[0],
                                'OverallF': OverallF[0],
                                'pval_OverallF': pval_OverallF[0],
                                'SSE': SSE[0],
                                'MSE': MSE[0],
                                'R2': R2[0],
                                'R2adj': R2a[0],
                                'BIC': BIC[0],
                                'AIC': AIC[0],
                                'Cp': Cp[0]
                                }))
            print('------------------------------------------------------')
            print(' ')
        if 'st' in model and 'in' in model['st'] and dsp == 'all':
            print('--- Partial model measures ---')
            Variable = c_(model['cname_i'])
            Estimates = model['pm']
            st = model['st']['in']
            if st is not None:
                n = len(st)
                T2SS = nans((n, 1))
                PartialF = nans((n, 1))
                pval_PartialF = nans((n, 1))
                PartialR2 = nans((n, 1))
                for i in np.arange(n):
                    T2SS[i] = st[i]['t2ss']
                    PartialF[i] = st[i]['Fp']
                    pval_PartialF[i] = st[i]['p_Fp']
                    PartialR2[i] = st[i]['R2prt']
                SandardError = model['st']['ovr']['STE']
                if not len(PartialF) == 0 and PartialF.shape == Variable.shape:
                    print(pd.DataFrame({'Variable': Variable[:, 0],
                                        'Estimates': Estimates[:, 0],
                                        'SandardError': SandardError[:, 0],
                                        'T2SS': T2SS[:, 0],
                                        'PartialR2': PartialR2[:, 0],
                                        'PartialF': PartialF[:, 0],
                                        'pval_PartialF': pval_PartialF[:, 0]
                                        }))
                else:
                    print('    Empty set...')
            else:
                print('    Empty set...')
            print('------------------------------------------------------')
            print(' ')
        if 'st' in model and 'out' in model['st'] and dsp == 'all':
            print('--- Measures of eligible to enter variables ---')
            Variable = c_(model['cname_o'])
            st = model['st']['out']
            n = len(st)
            T2SS = nans((n, 1))
            PartialF = nans((n, 1))
            pval_PartialF = nans((n, 1))
            PartialR2 = nans((n, 1))
            for i in np.arange(n):
                T2SS[i] = st[i]['t2ss']
                PartialF[i] = st[i]['Fp']
                pval_PartialF[i] = st[i]['p_Fp']
                PartialR2[i] = st[i]['R2prt']
            if not len(PartialF) == 0 and len(PartialF) == len(Variable):
                print(pd.DataFrame({'Variable': Variable[:, 0],
                                    'T2SS': T2SS[:, 0],
                                    'PartialR2': PartialR2[:, 0],
                                    'PartialF': PartialF[:, 0],
                                    'pval_PartialF': pval_PartialF[:, 0]
                                    }))
            else:
                print('    Empty set...')
            print('------------------------------------------------------')
            print(' ')
            ###################################################################################