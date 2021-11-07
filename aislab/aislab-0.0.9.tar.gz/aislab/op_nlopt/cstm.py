import numpy as np
from aislab.gnrl.bf import *

##############################################################################
##############################################################################
def f_cs(X, args):
    import copy
    from aislab.gnrl.sf import sort
    from aislab.dp_feng.binenc import cut
    from aislab.gnrl.measr import confm
    # Objective function for credit risk strategy optimization
    # needed for old GA
    case = 1
    if isinstance(X, list):
        case = -1
        X = np.array(X)
    # needed for old GA

    data = args['data']  # data set
    BRA = args['BRA']  # Desired Bad Rate in AA (less risky) risk zone
    BRR = args['BRR']  # Desired Bad Rate in RR (most risky) risk zone
    TA = args['TA']  # Desired Total number of applications in AA risk zone
    TR = args['TR']  # Desired Total number of applications in RR risk zone
    minNb = args['minNb']  # minimum number of Bad applications in each risk zone
    minNgb = args['minNgb']  # minimum number of Good & Bad applications in each risk zone
    mindBR = args['mindBR']  # minimum change in the Bad Rate moving from one risk zone to a neighbour zone
    w = args['w']  # vector containing the weights of all business requirements included in the objective function
    nc1 = args['nc1']  # number of cut-offs w.r.t. first (GB) scorecard
    nc2 = args['nc2']  # number of cut-offs w.r.t. second (GBR) scorecard
    lb1 = args['lb1']  # lower bound for cut-offs of the first scorecard
    lb2 = args['lb2']  # lower bound for cut-offs of the second scorecard
    ub1 = args['ub1']  # upper bound for cut-offs of the first scorecard
    ub2 = args['ub2']  # upper bound for cut-offs of the second scorecard
    minx = args['minx']  # upper bound for cut-offs of the first scorecard
    maxx = args['maxx']  # upper bound for cut-offs of the second scorecard
    if X.ndim == 1: X = np.array([X])
    N = len(X)
    F = np.full((N,), np.nan)
    i = 0
    for x in X:
        x1 = x[:nc1, ]
        x2 = x[nc1:, ]
        # x1, ss = sort(c_(x[:nc1, ]))
        # x2, ss = sort(c_(x[nc1:, ]))
        # minx = np.min([minx, np.min(x)])  # upper bound for cut-offs of the first scorecard
        # maxx = np.max([maxx, np.max(x)])  # upper bound for cut-offs of the second scorecard
        # x1 = (x1 - minx) / (maxx - minx) * (ub1 - lb1) + lb1
        # x2 = (x2 - minx) / (maxx - minx) * (ub2 - lb2) + lb2
        # x1 = np.round(x1.flatten())
        # x2 = np.round(x2.flatten())
        if len(set(x1)) != len(x1) or len(set(x2)) != len(x2): return case*np.inf  # if there are 2 or more the same GB cut-offs: F = inf
        try:
            GB_zones = cut(data['Score_GB'].values, x1).flatten()
            GBR_zones = cut(data['Score_GBR'].values, x2).flatten()
        except:
            print("In fobj(): Wrong cut-offs...")
        good = confm(-GB_zones, -GBR_zones, w=data['Good'].values).astype(int)  # confusion matrix
        bad = confm(-GB_zones, -GBR_zones, w=data['Bad'].values).astype(int)  # confusion matrix
        reject = confm(-GB_zones, -GBR_zones, w=data['Reject'].values).astype(int)  # confusion matrix
        import warnings
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        bad_rate = bad / (good + bad) * 100
        total_gb = good + bad
        total = good + bad + reject
        drBR = bad_rate[:, 1:] - bad_rate[:, :-1]  # rowwise delta BR
        dcBR = bad_rate[1:, :] - bad_rate[:-1, :]  # colwise delta BR

        mr, nr = np.shape(drBR)
        mc, nc = np.shape(dcBR)
        drBR1 = copy.deepcopy(drBR)
        for k in range(nr-1, 0, -1):
            for j in range(mr-1, 0, -1):
                if k-1 >= 0 and not np.isnan(drBR1[j, k]) and np.isnan(drBR1[j, k-1]): drBR1[j, k-1] = drBR1[j, k]
                if j-1 >= 0 and not np.isnan(drBR1[j, k]) and np.isnan(drBR1[j-1, k]): drBR1[j-1, k] = drBR1[j, k]
        dcBR1 = copy.deepcopy(dcBR)
        for k in range(nc-1, 0, -1):
            for j in range(mc-1, 0, -1):
                if k-1 >= 0 and not np.isnan(dcBR1[j, k]) and np.isnan(dcBR1[j, k-1]): dcBR1[j, k-1] = dcBR1[j, k]
                if j-1 >= 0 and not np.isnan(dcBR1[j, k]) and np.isnan(dcBR1[j-1, k]): dcBR1[j-1, k] = dcBR1[j, k]
        negdrBR = drBR1[drBR1 < mindBR]  # negative trend or not enough change in rowwise delta BR
        negdcBR = dcBR1[dcBR1 < mindBR]  # negative trend or not enough change in colwise delta BR

        # discriminatory power of the strategy  #  min(F1) = 0
        F1 = (((BRA - bad_rate[0, 0]) / max(1e-6, 100 - BRA)) ** 2 + ((TA - total[0, 0]) / max(1e-6, TA)) ** 2) / 2
        F2 = (((BRR - bad_rate[-1, -1]) / max(1e-6, BRR - 0)) ** 2 + ((TR - total[-1, -1]) / max(1e-6, TR)) ** 2) / 2
        # monotonicity of BR  #  min(F2) = 0
        F3 = ((np.sum(mindBR - negdrBR) + np.sum(mindBR - negdcBR)) / (nc1 * nc2)) ** 2
        # mininmum number of Bad and Good & Bad applications per segment  #  min(F4) = min(F5) = 0
        F4 = (np.sum((minNb - bad) * (minNb - bad > 0) * (total_gb > 0)) / max(1e-6,
                                                                               (nc1 + 1) * (nc2 + 1) * minNb)) ** 2
        F5 = (np.sum((minNgb - total_gb)*(minNgb - total_gb > 0)*(total_gb > 0))/max(1e-6, (nc1 + 1)*(nc2 + 1)*minNgb))**2
        # minimum number of NaN cells: min(F6) = 0
        F6 = (np.sum(np.sum(np.isnan(bad_rate))) / ((nc1 + 1) * (nc2 + 1))) ** 2
        # minimum number of records in most populated cell  # min(F7) = 0
        F7 = np.max(np.max(total)) / max(1e-6, sum(sum(total)))
        F[i] = w[0] * F1 + w[1] * F2 + w[2] * F3 + w[3] * F4 + w[4] * F5 + w[5] * F6 + w[6] * F7

        if np.isnan(F[i]):
            F[i] = case * np.inf
            return F
        i += 1
        # needed for old GA
        if len(F) == 1: F = -F[0]
        if isinstance(F, float) and np.isinf(F): F = -np.inf
        # needed for old GA
    return F
##############################################################################
##############################################################################
###################################################################################

# exp1:                                                 # y = a + b*e^x
# exp2:                                                 # y = a + b*e^(x + c)
# exp3:   ym = pm[0] + pm[1]*np.exp(x*pm[2])            # y = a + b*e^(x*c)

# log:    ym = pm[0] + pm[1]*np.log(abs(x) + 1)         # ym = a + b*ln(x)
# log1:   ym = pm[0] + pm[1]*np.log(pm[2]*abs(x) + 1)   # y = a + b*ln(c*|x| + 1)
# logW:   ym = pm[0] + pm[1]*np.log(abs(pm[2]*x + 1))   # y = a + b*ln(|c*x + 1|)

# lgr:    ym = 1/(1 + np.exp(-x@pm))                    # y = 1/(1 + e^-(x*pm))

# exp model
# args['b'] = 1e-8
# args['c'] = 1e3
# log model
# args['b'] = 0.01
# args['c'] = 1e3

def f_exp1(args):
    # F for model: y = a + b*e^x
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    pm = args['x']
    if x.shape[1] == 0: x = c_(x)
    ym = exp1_apl(x, args['x'])
    e = y - ym
    F = e.T@(e*w)
    args['data'][:, -1] = ym.flatten()

    b = args['b']
    c = args['c']
    A = np.diag((pm.flatten() < b))*c
    F = F + pm.T@A@pm

    return F, args
###################################################################################
def f_exp2(args):
    # F for model: y = a + b*e^(x + c)
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    pm = args['x']
    if x.shape[1] == 0: x = c_(x)
    ym = exp2_apl(x, pm)
    e = y - ym
    F = e.T@(e*w)
    args['data'][:, -1] = ym.flatten()

    b = args['b']
    c = args['c']
    dd = np.hstack((pm.flatten()[:2], zeros((1,))))
    A = np.diag((dd < b))*c
    F = F + pm.T@A@pm

    return F, args
###################################################################################
def f_exp3(args):
   # F for model: y = a + b*e^(x*c)
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    pm = args['x']
    if x.shape[1] == 0: x = c_(x)
    ym = exp3_apl(x, pm)
    e = y - ym
    F = e.T@(e*w)
    args['data'][:, -1] = ym.flatten()

    # print(np.hstack((e, w)))

    b = args['b']
    c = args['c']
    d1 = pm.flatten()
    d2 = (1 - (pm[0, 0] + pm[1, 0]))**2*c
    A = np.diag((d1 < b))*c
    F = F + pm.T@A@pm + d2

    return F, args
###################################################################################
def f_lgr(args):
    # F for logistic regression model: ym = 1/(1 + exp(-x*pm))
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    pm = args['x']
    ym = lgr_apl(x, pm)
    ym[ym > 1 - 1e-10] = 1 - 1e-10
    ym[ym < 1e-10] = 1e-10
    m = pm.shape[1]
    yy = np.matlib.repmat(y, 1, m)
    ww = np.matlib.repmat(w, 1, m)
    F = -sum(yy*np.log(ym)*ww + (1 - yy)*np.log(1 - ym)*ww)
    args['data'][:, -1] = ym.flatten()
    return F, args
###################################################################################
def f_log1(args):
    # F for exponential model: ym = a + b*ln(x)
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    if x.shape[1] == 0: x = c_(x)
    ym = log1_apl(x, args['x'])
    e = y - ym
    F = e.T@(e*w)
    args['data'][:, -1] = ym.flatten()

    pm = args['x']
    b = args['b']
    c = args['c']
    A = np.diag((pm.flatten() < b))*c
    F = F + pm.T@A@pm

    return F, args
###################################################################################
def f_log2(args):
    # F for exponential model: ym = a + b*ln(x)
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    if x.shape[1] == 0: x = c_(x)
    ym = log2_apl(x, args['x'])
    e = y - ym
    F = e.T@(e*w)
    args['data'][:, -1] = ym.flatten()

    pm = args['x']
    b = args['b']
    c = args['c']
    A = np.diag((pm.flatten() < b))*c
    F = F + pm.T@A@pm

    return F, args
###################################################################################
def f_log3(args):
    # F for exponential model: ym = a + b*ln(c*x + 1)
    pm = args['x']
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    if x.shape[1] == 0: x = c_(x)
    ym = log3_apl(x, args['x'])
    e = y - ym
    F = e.T@(e*w)
    args['data'][:, -1] = ym.flatten()

    b = args['b']
    c = args['c']
    d1 = pm.flatten()
    d2 = (pm[0, 0] - 1)**2*c

    A = np.diag((d1 < b))*c
    F = F + pm.T@A@pm + d2

    return F, args
###################################################################################
def g_exp1(args=None):
    # ---------------------------------------------
    # Author: Alexander Efemov
    # Date:   20.12.2009
    # Course: Modelling and Processes Optimization
    # ---------------------------------------------
    # gradient of F for model: y = a + b*e^x
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    ym = c_(args['data'][:, -1])
    e = y - ym
    g = np.zeros((2, 1))
    g[0] = (-2*w.T@e)[0, 0]
    g[1] = (-2*(w*e).T@np.exp(x))[0]

    pm = args['x']
    b = args['b']
    c = args['c']
    A = np.diag((pm.flatten() < b))*c
    g = g + 2*A@pm

    return g
###################################################################################
def g_exp2(args=None):
    # ---------------------------------------------
    # Author: Alexander Efemov
    # Date:   20.12.2009
    # Course: Modelling and Processes Optimization
    # ---------------------------------------------
    # gradient of F model: y = a + b*e^(x + c)
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    ym = c_(args['data'][:, -1])
    pm = args['x']
    e = y - ym
    tmp = np.exp(x + pm[2])
    g = np.zeros((len(pm), 1))
    g[0] = (-2*w.T@e)[0, 0]
    g[1] = (-2*(w*e).T@tmp)[0]
    g[2] = (-2*pm[1]*(w*e).T@tmp)[0]

    b = args['b']
    c = args['c']
    dd = np.hstack((pm.flatten()[:2], zeros((1,))))
    A = np.diag((dd < b))*c
    g = g + 2*A@pm

    return g
###################################################################################
def g_exp3(args=None):
    # ---------------------------------------------
    # Author: Alexander Efemov
    # Date:   20.12.2009
    # Course: Modelling and Processes Optimization
    # ---------------------------------------------
    # gradient of F for model: y = a + b*e^(x*c)
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    ym = c_(args['data'][:, -1])
    pm = args['x']
    e = y - ym
    tmp = np.exp(x*pm[2])
    g = np.zeros((len(pm), 1))
    g[0] = (-2*w.T@e)[0, 0]
    g[1] = (-2*(w*e).T@tmp)[0]
    g[2] = (-2*pm[1]*(w*e*x).T@tmp)[0]

    b = args['b']
    c = args['c']
    dd = pm.flatten()
    A = np.diag((dd < b))*c
    g = g + 2*A@pm + np.array([[-2*(1 - (pm[0,0] + pm[1,0]))*c], [-2*(1 - (pm[0,0] + pm[1,0]))*c], [0]])
    return g
###################################################################################
def g_lgr(args=None):
    # ---------------------------------------------
    # Author: Alexander Efemov
    # Date:   20.12.2009
    # Course: Modelling and Processes Optimization
    # ---------------------------------------------
    # gradient of F for logistic regression model: ym = 1/(1 + exp(-x*pm))
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    ym = c_(args['data'][:, -1])
    g = -x.T@((y - ym)*w)
    return g
###################################################################################
def g_log1(args=None):
    # gradient of F for log model: ym = 1/(1 + exp(-x*pm))
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    ym = c_(args['data'][:, -1])
    e = y - ym
    g = np.zeros((2, 1))
    g[0] = (-2*w.T@e)[0, 0]
    g[1] = (-2*(w*e).T@np.log(abs(x) + 1))[0]

    pm = args['x']
    b = args['b']
    c = args['c']
    A = np.diag((pm.flatten() < b))*c
    g = g + 2*A@pm

    return g
###################################################################################
def g_log3(args=None):
    # ---------------------------------------------
    # Author: Alexander Efemov
    # Date:   20.12.2009
    # Course: Modelling and Processes Optimization
    # ---------------------------------------------
    # gradient of F for logistic regression model: ym = 1/(1 + exp(-x*pm))
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    ym = c_(args['data'][:, -1])
    pm = args['x']
    e = y - ym
    g = np.zeros((len(pm), 1))
    g[0] = (-2*w.T@e)[0, 0]
    g[1] = (-2*(w*e).T@np.log(abs(pm[2]*x) + 1))[0]
    g[2] = ((-2*pm[1]*(w*e/(abs(pm[2]*x) + 1)).T@x)*np.sign(pm[2]*x + 1))[0]  # !!!: np.sign(0) = 0

    b = args['b']
    c = args['c']
    dd = pm.flatten()
    A = np.diag((dd < b))*c
    d2 = (pm[0, 0] - 1)**2*c
    g = g + 2*A@pm + np.array([[2*(pm[0,0] - 1)*c], [0], [0]])
    return g
###################################################################################
def h_exp1(args=None):
    # ---------------------------------------------
    # Author: Alexander Efemov
    # Date:   20.12.2009
    # Course: Modelling and Processes Optimization
    # ---------------------------------------------
    # Hessian of F for model: y = a + b*e^x
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    w = c_(args['data'][:, -2])
    ym = c_(args['data'][:, -1])
    H = np.zeros(shape = (2,2))
    tmp = np.exp(x)
    H[0, 0] = 2*np.sum(w)
    H[0, 1] = 2*(w.T@tmp)[0]
    H[1, 0] = H[0, 1]
    H[1, 1] = 2*((w*tmp).T@tmp)[0]

    pm = args['x']
    b = args['b']
    c = args['c']
    A = np.diag((pm.flatten() < b))*c
    H = H + 2*A

    return H
###################################################################################
def h_exp2(args=None):
    # ---------------------------------------------
    # Author: Alexander Efemov
    # Date:   20.12.2009
    # Course: Modelling and Processes Optimization
    # ---------------------------------------------
    # Hessian of F for model: y = a + b*e^(x + c)
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    w = c_(args['data'][:, -2])
    y = c_(args['data'][:, -3])
    ym = c_(args['data'][:, -1])
    pm = args['x']
    e = y - ym
    H = np.zeros(shape=(3, 3))
    tmp = np.exp(x + pm[2])
    H[0, 0] = 2*np.sum(w)
    H[0, 1] = 2*(w.T@tmp)[0]
    H[0, 2] = 2*pm[1]*(w.T@tmp)[0]
    H[1, 0] = H[0, 1]
    H[1, 1] = 2*((w*tmp).T@tmp)[0]
    H[1, 2] = 2*pm[1]*((w*tmp).T@tmp)[0] - 2*((w*e).T@tmp)[0]
    H[2, 0] = H[0, 2]
    H[2, 1] = H[1, 2]
    H[2, 2] = 2*pm[1]**2*((w*tmp).T@tmp)[0] - 2*pm[1]*((w*e).T@tmp)[0]

    pm = args['x']
    b = args['b']
    c = args['c']
    dd = np.hstack((pm.flatten()[:2], zeros((1,))))
    A = np.diag((dd < b))*c
    H = H + 2*A
    return H
    dd = pm.flatten()
    A = np.diag((dd < b))*c
###################################################################################
def h_exp3(args=None):
    # ---------------------------------------------
    # Author: Alexander Efemov
    # Date:   20.12.2009
    # Course: Modelling and Processes Optimization
    # ---------------------------------------------
    # Hessian of F for model: y = a + b*e^(x*c)
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    w = c_(args['data'][:, -2])
    y = c_(args['data'][:, -3])
    ym = c_(args['data'][:, -1])
    pm = args['x']
    e = y - ym
    H = np.zeros(shape=(3, 3))
    tmp = np.exp(x*pm[2])
    H[0, 0] = 2*np.sum(w)
    H[0, 1] = 2*(w.T@tmp)[0]
    H[0, 2] = 2*pm[1]*((w*x).T@tmp)[0]
    H[1, 0] = H[0, 1]
    H[1, 1] = 2*((w*tmp).T@tmp)[0]
    H[1, 2] = 2*pm[1]*((w*tmp*x).T@tmp)[0] - 2*((w*e*x).T@tmp)[0]
    H[2, 0] = H[0, 2]
    H[2, 1] = H[1, 2]
    H[2, 2] = 2*pm[1]**2*((w*tmp*x**2).T@tmp)[0] - 2*pm[1]*((w*e*x**2).T@tmp)[0]

    pm = args['x']
    b = args['b']
    c = args['c']
    dd = pm.flatten()
    A = np.diag((dd < b))*c
    H = H + 2*A + np.array([[2*c, 2*c, 0], [2*c, 2*c, 0], [0, 0, 0]])
    return H
###################################################################################
def h_lgr(args=None):
    # ---------------------------------------------
    # Author: Alexander Efemov
    # Date:   20.12.2009
    # Course: Modelling and Processes Optimization
    # ---------------------------------------------
    # Hessian of F for logistic regression model: ym = 1/(1 + exp(-x*pm))
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    w = c_(args['data'][:, -2])
    ym = c_(args['data'][:, -1])
    n = x.shape[1]
    H = (x*np.matlib.repmat(ym*(1 - ym)*w, 1, n)).T@x
    return H
###################################################################################
def h_log1(args=None):
    # ---------------------------------------------
    # Author: Alexander Efemov
    # Date:   20.12.2009
    # Course: Modelling and Processes Optimization
    # ---------------------------------------------
    # Hessian of F for logistic regression model: ym = 1/(1 + exp(-x*pm))
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    w = c_(args['data'][:, -2])
    ym = c_(args['data'][:, -1])
    H = np.zeros(shape = (2,2))
    tmp = np.log(abs(x) + 1)
    H[0, 0] = 2*np.sum(w)
    H[0, 1] = 2*(w.T@tmp)[0]
    H[1, 0] = H[0, 1]
    H[1, 1] = 2*((w*tmp).T@tmp)[0]

    pm = args['x']
    b = args['b']
    c = args['c']
    A = np.diag((pm.flatten() < b))*c
    H = H + 2*A
    return H
###################################################################################
def h_log3(args=None):
    # ---------------------------------------------
    # Author: Alexander Efemov
    # Date:   20.12.2009
    # Course: Modelling and Processes Optimization
    # ---------------------------------------------
    # Hessian of F for logistic regression model: ym = 1/(1 + exp(-x*pm))
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    w = c_(args['data'][:, -2])
    y = c_(args['data'][:, -3])
    ym = c_(args['data'][:, -1])
    pm = args['x']
    e = y - ym
    H = np.zeros(shape=(3, 3))
    tmp = np.log(abs(pm[2]*x + 1))
    H[0, 0] = 2*np.sum(w)
    H[0, 1] = 2*(w.T@tmp)[0]
    H[0, 2] = (2*pm[1]*((w/abs(pm[2]*x + 1)).T@x)*np.sign(pm[1]*x + 1))[0]
    H[1, 0] = H[0, 1]
    H[1, 1] = 2*((w*tmp).T@tmp)[0]
    H[1, 2] = (2*pm[1]*((w*tmp/abs(pm[2]*x + 1)).T@x)*np.sign(pm[1]*x + 1) - 2*((w*e/abs(pm[2]*x + 1)).T@x)*np.sign(pm[1]*x + 1))[0]
    H[2, 0] = H[0, 2]
    H[2, 1] = H[1, 2]
    H[2, 2] = 2*pm[1]**2*((w/abs(pm[2]*x + 1)*x).T@x)[0] - 2*pm[1]*((w*e*x/abs(pm[2]*x + 1)).T@x)[0]

    pm = args['x']
    b = args['b']
    c = args['c']
    dd = pm.flatten()
    A = np.diag((dd < b))*c
    H = H + 2*A + np.array([[2*c, 0, 0], [0, 0, 0], [0, 0, 0]])
    return H
###################################################################################
def exp1_apl(x, pm):
    # model: y = a + b*e^x
    ym = pm[0] + pm[1]*np.exp(x)
    return ym
###################################################################################
def exp2_apl(x, pm):

    ym = pm[0] + pm[1]*np.exp(x + pm[2])
    return ym
###################################################################################
def exp3_apl(x, pm):
    # model: y = a + b*e^(x*c)
    ym = pm[0] + pm[1]*np.exp(x*pm[2])
    return ym
###################################################################################
def lgr_apl(x, pm):
    # logistic regression function
    if not isinstance(x, np.ndarray): x = np.array([[x]])
    if not isinstance(pm, np.ndarray): pm = np.array([[pm]])
    ym = 1/(1 + np.exp(-x@pm))
    return ym
###################################################################################
def log1_apl(x, pm):
    ym = pm[0] + pm[1]*np.log(abs(x) + 1)
    return ym
###################################################################################
def log2_apl(x, pm):
    ym = pm[0] + pm[1]*np.log(pm[2]*abs(x) + 1)
    return ym
###################################################################################
def log3_apl(x, pm):
    ym = pm[0] + pm[1]*np.log(abs(pm[2]*x + 1))
    return ym
###################################################################################
