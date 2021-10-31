"""
    author: OPEN-MAT
    date: 	15.06.2019
    Matlab version: 26 Apr 2009
    Course: Multivariable Control Systems
"""
import numpy as np
from numpy import matlib

from aislab.gnrl.bf import * # c_
from aislab.gnrl.sf import *
from aislab.gnrl.measr import *  # vaf
from aislab.op_nlopt import stopcrt

##############################################################################
# def dm2dv():
##############################################################################
def dmpm(U=np.empty((0, 0)),
         Y=np.empty((0, 0)),
         E=np.empty((0, 0)),
         na=None,
         nb=None,
         nc=None,
         pm0=None,
         par={}
         ):
    """
     DM2M constructs the data matrix for a model in a parameter matrix form.
     F = dmpm(U, Y, E, na, nb, nc)
     
     Inputs:
       U - [N x m] input data matrix with structure
           U = [u(1) u(n + 2) ... u(N)]'
           where N is the length of the observation interval and u(i) is m dimensional vectos
       Y - [N x r] output data matrix with structure
           Y = [y(1) y(2) ... y(N)]',
       E - [N x r] residual data matrix with structure
           E = [e(1) e(2) ... e(N)]',
       par - structure with fields:
         na - maximum degree of polynomials in A(q^-1)
         nb - maximum degree of polynomials in B(q^-1)
         nc - maximum degree of polynomials in C(q^-1)
         intercept - 1 if model has intercept, otherwise 0. Default is 0.
    
     Outputs:
       F - [N - n x z] data matrix /z = na*r + nb*m + nc*r/
    """

    if type(U) != np.ndarray:   U = np.array([U])
    if type(Y) != np.ndarray:   Y = np.array([Y])
    if type(E) != np.ndarray:   E = np.array([E])
    N = int()
    if len(U) > 0:
        N, m = U.shape
    else:
        m = 0
    if len(Y) > 0:
        N, r = Y.shape
    else:
        r = 0
    if len(E) > 0: N, r = E.shape
    if not N > 0:
        print('In DMPM: At least one data matrix should be not empty...')
        return None

    if (np.array([na == None])).any():
        if 'na' in par:
            na = par['na']
        else:
            na = np.zeros((r, 1))
    if (np.array([nb == None])).any():
        if 'nb' in par:
            nb = par['nb']
        else:
            nb = np.zeros((1, m))
    if (np.array([nc == None])).any():
        if 'nc' in par:
            nc = par['nc']
        else:
            nc = np.zeros((r, 1))
    if (np.array([pm0 == None])).any():
        if 'pm0' in par:
            pm0 = par['pm0']
        else:
            pm0 = np.zeros((r, 1))

    if isinstance(nb, np.ndarray) and nb.shape[1] == 0: nb = 0
    na = int(np.max(na))  # Current dmpm() works with na, nb, nc - scalars, todo: should work with 1D arrays
    nb = int(np.max(nb))
    nc = int(np.max(nc))
    pm0 = int(np.max(pm0))
    n = np.max([na, nb, nc])
    Fi = np.ones((N - n, pm0))
    Fy = nans((N - n, na * r))
    if na > 0 and Y.size > 0:
        for i in range(na - 1, -1, -1):
            Fy[:, (na - i - 1) * r:(na - i) * r] = -Y[(n - na + i):(N - na + i)]
    Fu = nans((N - n, nb * m))
    if nb > 0 and U.size > 0:
        for i in range(nb - 1, -1, -1):
            Fu[:, (nb - i - 1) * m:(nb - i) * m] = U[(n - nb + i):(N - nb + i)]
    Fe = nans((N - n, nc * r))
    if nc > 0 and E.size > 0:
        for i in range(nc - 1, -1, -1):
            Fe[:, (nc - i - 1) * r:(nc - i) * r] = E[(n - nc + i):(N - nc + i)]
    return np.hstack((Fi, Fy, Fu, Fe))


##############################################################################
def dmpv(U=np.empty((0, 0)), Y=np.empty((0, 0)), E=np.empty((0, 0)),
         na=None,
         nb=None,
         nc=None,
         pm0=None,
         m_dense=1,
         par={}
         ):
    if type(U) != np.ndarray:   U = np.array([U])
    if type(Y) != np.ndarray:   Y = np.array([Y])
    if type(E) != np.ndarray:   E = np.array([E])
    N = int()
    if len(U) > 0:
        N, m = U.shape
    else:
        m = 0
    if len(Y) > 0:
        N, r = Y.shape
    else:
        r = 0
    if len(E) > 0: N, r = E.shape
    if not N > 0:
        print('In DMPV: At least one data matrix should be not empty...')
        return None

    if isinstance(na, (int, float)):  na = np.full([r, r], na)
    if isinstance(nb, (int, float)):  nb = np.full([r, m], nb)
    if isinstance(nc, (int, float)):  nc = np.full([r, r], nc)
    if isinstance(pm0, (int, float)): pm0 = np.full([r, 1], pm0)
    if (np.array([na == None])).any():
        if 'na' in par:
            na = par['na']
        else:
            na = np.zeros((r, r))
    if (np.array([nb == None])).any():
        if 'nb' in par:
            nb = par['nb']
        else:
            nb = np.zeros((r, m))
    if (np.array([nc == None])).any():
        if 'nc' in par:
            nc = par['nc']
        else:
            nc = np.zeros((r, r))
    if (np.array([pm0 == None])).any():
        if 'pm0' in par:
            pm0 = par['pm0']
        else:
            pm0 = np.zeros((r, 1))

    n = int(np.max([np.max(na), np.max(nb), np.max(nc)]))

    Int = np.tile(pm0.T, (N, 1))
    ni = np.diag(pm0.flatten());

    if m_dense == 1:
        F = np.empty(((N - n) * r, 0))
        for i in range(r):
            MM = np.empty((N - n, 0))
            M = np.empty((N - n, 0))
            for factors, nn in enumerate([ni, na, nb, nc]):
                if factors == 0:
                    M = Int
                elif factors == 1:
                    M = -Y
                elif factors == 2:
                    M = U
                elif factors == 3:
                    M = E
                if nn.size > 0 and M.size > 0:
                    rr = nn.shape[1]
                    nn = nn.astype(int)
                    for j in range(rr):
                        if nn[i, j] > 0:
                            if n + 1 > N:
                                Mi = M[:, j]
                            else:
                                Mi = M[:, j].T
                            for ii in range(nn[i, j]):
                                Mi = np.roll(M[:, j], ii + 1, axis=0)[n:].reshape((N - n, 1))
                                MM = np.hstack((MM, Mi))
            sni = np.sum(ni[i], initial=0)
            sna = np.sum(na[i], initial=0)
            snb = np.sum(nb[i], initial=0)
            snc = np.sum(nc[i], initial=0) if nc.size > 0 else 0
            pi = sni + sna + snb + snc
            Fi = np.zeros(((N - n) * r, int(pi)))
            Fi[range(i, (N - n) * r, r)] = MM
            F = np.hstack((F, Fi))
        return F
##############################################################################
# todo: make dv2dm() faster - skip for->for
def dv2dm(x, cols):
    if x.shape[0] % cols != 0:
        print('Incorect data dimensions...')
        return None
    rows = int(x.shape[0] / cols)
    X = nans((rows, cols))
    current_pos = 0
    for row in range(0, rows):
        for column in range(0, cols):
            X[row][column] = x[current_pos]
            current_pos += 1
    return X
##############################################################################
def elspm(U, Y, na=0, nb=0, nc=0, pm0=0, maxiter=50, axcnv=None, xcnv=1e-8, afcnv=None, fcnv=1e-8, gcnv=None, dsp=False):
    N, r = Y.shape
    n = max(na, nb, nc)
    nn = n - max(na, nb)

    Parx = lspm(U, Y, na, nb, pm0)
    Farx = dmpm(U[nn:], Y[nn:], na=na, nb=nb, nc=0, pm0=pm0)
    E = np.vstack((np.zeros([n, r]), Y[n:, :] - lin_apl(Farx, Parx)))
    f = np.sum(np.diag(E.T@E) / N)
    # if nc == 0: return Pm, E
    Pm = np.vstack((Parx, np.zeros([r*nc, r])))
    itr = 0
    iterate = 1
    while iterate:
        itr += 1
        F = np.hstack((Farx, dmpm(E=E, nc=nc)))
        Pm_1 = Pm
        Pm = nsinv(F.T@F)@F.T@Y[n:]
        E = np.vstack((np.zeros((n, r)), Y[n:] - F@Pm))
        f_1 = f
        f = np.sum(np.diag(E.T@E) / N)
        Pm1 = np.empty((0, 0))
        if f > f_1:
            Pm1 = Pm_1
            Pm = (Pm + Pm_1) / 2
            E = np.vstack((np.zeros((n, r)), Y[n:] - F@Pm))
            if dsp == True:
                print('\n iter: ', itr, '\n Reduce step size...')
        iterate, msg = stopcrt(x=Pm, F=f, xx=Pm_1, FF=f_1, itr=itr, maxiter=50, xcnv=1e-8, fcnv=1e-8)
    if dsp == True:
        print("It took [elspm.py]", itr, "iterations to reach the end condition.")
        print(maxiter, "is the maximum number of iterations.")
    return Pm, E
##############################################################################
def armax_apl(U, Y=None, E=None, pm=None, na=0, nb=0, nc=0, pm0=0, sim=False, ltv=False):
    if isinstance(nb, (int, float)):
        r = pm.shape[1]
        m = U.shape[1]
        mtype = 'PM'
    else:
        r = nb.shape[0]
        m = nb.shape[1]
        mtype = 'PV'
    if mtype == 'PV': pm = pv2m(pm, na, nb, nc, pm0=pm0) # if model in PV form --> goto PM form
    nn = np.max(np.hstack((na, nb, nc)))
    if not sim:
        if nn == 0:
            if pm0: U = np.hstack((np.ones((U.shape[0], 1)), U))
            ym = lin_apl(U, pm)
        else:
            F = dmpm(U, Y, E, na, nb, nc, pm0)
            ym = lin_apl(F, pm)
    else:
        N = U.shape[0]
        r = pm.shape[1]
        if E is None: E = zeros((N, r))
        ym = np.zeros((N, r))
        for k in range(nn, N):
            fi = dmpm(U[k - nn:k + 1, :], ym[k - nn:k + 1, :], E[k - nn:k + 1, :], na, nb, nc, pm0)
            ym[k, :] = fi@pm + r_(E[k, :])
    return ym


##############################################################################
def elspv(U, Y, na=0, nb=0, nc=0, pm0=0, maxiter=50, axcnv=None, xcnv=1e-8, afcnv=None, fcnv=1e-8, gcnv=None, dsp=False):
    N, r = Y.shape
    if len(U) > 0:  m = U.shape[1]
    else:           m = 0
    if isinstance(na, (int, float)):  na = np.full([r, r], na)
    if isinstance(nb, (int, float)):  nb = np.full([r, m], nb)
    if isinstance(nc, (int, float)):  nc = np.full([r, r], nc)
    if isinstance(pm0, (int, float)): pm0 = np.full([r, 1], pm0)
    n = int(np.max(np.hstack((na, nb, nc))))
    nn = int(n - np.max(np.hstack((na, nb))))

    parx = lspv(U, Y, na=na, nb=nb, pm0=pm0)
    Ymab = arx_apl(U[nn:], Y[nn:], parx, na=na, nb=nb, pm0=pm0)
    # if nc.size == 0:  E = np.empty((0, 0));  return arx, E
    Fab = dmpv(U[nn:], Y[nn:], na=na, nb=nb, nc=np.zeros((nc.shape)), pm0=pm0)
    E = np.vstack((np.zeros([n, r]), Y[n:] - Ymab))
    f = np.sum(np.diag(E.T@E)/N)
    pm = np.vstack((parx, np.zeros((int(np.sum(nc)), 1))))
    Pm = np.vstack((pv2m(pm, na=na, nb=nb, pm0=pm0), np.zeros((r * int(np.max(nc)), r))))
    itr = 0
    iterate = 1
    while iterate:
        itr += 1
        F = dmpv(U, Y, E, na=na, nb=nb, nc=nc, pm0=pm0)  # todo: sparse
        pm_1 = pm
        Pm_1 = Pm
        pm = nsinv(F.T@F)@F.T@vec(Y[n:].T)  # to-do: sparse
        Pm = pv2m(pm, na=na, nb=nb, nc=nc, pm0=pm0)
        Ym = dv2dm(F@pm, r)
        E = np.vstack((np.zeros([n, r]), Y[n:] - Ym))
        F = dmpv(U, Y, E, na=na, nb=nb, nc=nc, pm0=pm0)
        f_1 = f
        f = np.sum(np.diag(E.T@E) / N)
        if f > f_1:
            pm1 = pm_1
            pm = c_(pm)
            pm = (pm + pm_1) / 2
            if dsp:
                print('iter: ', itr, ' Reduce step size!')
        iterate, msg = stopcrt(x=Pm, F=f, xx=Pm_1, FF=f_1, itr=itr, maxiter=50, xcnv=1e-8, fcnv=1e-8)
    pm = pm1 if f > f_1 else pm
    return pm, E
##############################################################################
# glspm():
# glspm_apl():
# glspv():
# glspv_apl():
# ivpm():
# ivpm_apl():
# ivpv():
# ivpv_apl():
# linreg OR ar, arx, armax, sarimax...
##############################################################################
def lspm(U, Y, na=0, nb=0, pm0=False, w=None):
    """
    Parameters
    ----------
    U : array, matrix
        input data matrix
    Y : array, matrix
        output data matrix
    par : dict; optional
        dictionary. The default is {'na':0, 'nb':0, 'pm0':False}.

    Returns
    -------
    Pm : TYPE
        DESCRIPTION.

    Description
    -----------
     LSPV calculates Least Squares (LS) estimates of ARX model in parameter matrix form.
     In case of static model factors are in matrix is U.
     mod = lspm_fit(U, Y, na, nb) determines the LS-estimates of ARX model
        A(q^-1)*yk = B(q^-1)*uk + ek
     represented in a parameter matrix form
        yk = Pm'*fk + ek,
     where:
        A(q^-1) is [el x el] polynomial matrix
           A(q^-1) = I + A1*q^-1 + ...  + Ana*q^-na 
        B(q^-1) is [el x m] polynomial matrix
           B(q^-1) = 0 + B1*q^-1 + ...  + Bnb*q^-nb
        na and nb are the maximum degrees of the polynomials in A(q^-1) and B(q^-1)
        respectively
        k - current time instant.
        uk - input vector in the k-th time instant /with m elements/
        yk - output vector in the k-th time instant /with el elements/
        ek - residual vector in the k-th time instant  /with el elements/
        fk - regression vector with [el*na + m*nb] elements in the k-th
        Pm - parameter matrix

     Inputs: 
       Y - [N x el] output data matrix with structure
           Y = [y(1) y(2) ... y(N)]',
           where N is the length of the observation interval
       U - [N x m] input data matrix with structure
           U = [u(1) u(2) ... u(N)]'
       w - [N x 1] input weight (optional - if no weight, then w = [])
       par - structure with fields:
         na - polynomials degree in A(q^-1)
         nb - polynomials degree in B(q^-1)
         intercept - 1 if model has intercept, otherwise 0. Default is 0.
    
     Outputs: 
        mod.Pm - [el*na + m*nb x el] matrix, containing the estimates of the model parameters
             Pm = [A1 A2 ... Ana B1 B2 ... Bnb]'
        mod.par
    """

    n = max(na, nb)
    N = len(Y)
    Pm = np.empty((0, 0))
    if max(na, nb) == 0:
        if pm0: U = np.hstack((np.ones((U.shape[0], 1)), U))
        if w is None:
            Pm = nsinv(U.T @ U) @ U.T @ Y
        else:
            W = np.diag(w[n:N].flatten())
            Pm = nsinv(U.T @ W @ U) @ U.T @ W @ Y[n:N][:]
    else:
        F = dmpm(U, Y, na=na, nb=nb, nc=0, pm0=pm0)
        if w == None:
            Pm = nsinv(F.T @ F) @ F.T @ Y[n:N][:]
        else:
            W = np.diag(w[n:N])
            Pm = nsinv(F.T @ W @ F) @ F.T @ W @ Y[n:N][:]
    return Pm
##############################################################################
def lin_apl(x, pm):
    return x@pm
##############################################################################
def arx_apl(U, Y=None, pm=None, na=0, nb=0, pm0=0, sim=False, ltv=False, E=None):
    if isinstance(nb, (int, float)):
        r = pm.shape[1]
        m = U.shape[1]
        mtype = 'PM'
    else:
        r = nb.shape[0]
        m = nb.shape[1]
        mtype = 'PV'
    if mtype == 'PV': pm = pv2m(pm, na, nb, pm0=pm0) # if model in PV form --> goto PM form
    nn = np.max(np.hstack((na, nb)))
    if not sim:
        if nn == 0:
            if pm0: U = np.hstack((np.ones((U.shape[0], 1)), U))
            ym = lin_apl(U, pm)
        else:
            F = dmpm(U, Y, na=na, nb=nb, nc=0, pm0=pm0)
            ym = lin_apl(F, pm)
    else:
        N = U.shape[0]
        if not ltv: r = pm.shape[1]
        else:       r = na.shape[0]
        if E is None: E = zeros((N, r))
        ym = np.zeros((N, r))
        if ltv:
            for k in range(nn, N):
                fi = dmpm(U[k - nn:k + 1, :], ym[k - nn:k + 1, :], na=na, nb=nb, pm0=pm0)
                ym[k, :] = fi@pv2m(pm[:, k], na, nb, pm0=pm0) + r_(E[k, :])
        else:
            for k in range(nn, N):
                fi = dmpm(U[k - nn:k + 1, :], ym[k - nn:k + 1, :], na=na, nb=nb, pm0=pm0)
                ym[k, :] = fi@pm + r_(E[k, :])
    return ym
##############################################################################
def lspv(U=np.empty((0, 0)),
         Y=np.empty((0, 0)),
         na=0,
         nb=0,
         pm0=0):
    N, r = Y.shape
    if len(U) > 0:
        N, m = U.shape
    else:
        m = 0
    if len(Y) > 0:
        N, r = Y.shape
    else:
        r = 0
    if not N > 0:
        print('In ELSPV: At least one data matrix should be not empty...')
        return None
    if isinstance(na, (int, float)):  na = np.full([r, r], na)
    if isinstance(nb, (int, float)):  nb = np.full([r, m], nb)
    if isinstance(pm0, (int, float)): pm0 = np.full([r, 1], pm0)
    F = dmpv(U, Y, na=na, nb=nb, pm0=pm0)
    n = int(np.max(np.hstack((na, nb))))
    if n == 0:
        pm = np.empty((0, 0))
    else:
        pm = nsinv(F.T@F)@F.T@vec(Y[n:].T)
    return c_(pm)
##############################################################################
def pm2v(Pm, na=None, nb=None, nc=0, pm0=0):
    # todo: include nc and pm0
    r = m = 1
    z = na + nb
    if z == 0: return np.empty((1, 1))
    pm = np.array(())
    for i in range(0, r):
        pari = Pm[:, i]
        if na > 0:
            for j in range(0, r):
                pij = pari[j + j:r * na + j:r]
                pm = np.hstack((pm, pij))
        if nb > 0:
            for j in range(0, m):
                pij = pari[j + j + r * na:m * nb + j + r * na:m]
                pm = np.hstack((pm, pij))
    return c_(pm)
##############################################################################
def pv2m(pm,
         na=None,
         nb=None,
         nc=None,
         pm0=None,
         par={}):
    if not np.array([nb == None]).any():
        r, m = nb.shape
    elif not np.array([na == None]).any():
        r = na.shape[0]
        m = 0
    elif not np.array([nc == None]).any():
        r = nc.shape[0]  # todo: use try-except --> at least one of {na, nb, nc} should be provided
        m = 0
    if np.array([na == None]).any():
        if 'na' in par:
            na = par['na']
        else:
            na = np.zeros((r, r))
    if np.array([nb == None]).any():
        if 'nb' in par:
            nb = par['nb']
        else:
            nb = np.zeros((r, m))
    if np.array([nc == None]).any():
        if 'nc' in par:
            nc = par['nc']
        else:
            nc = np.zeros((r, r))
    if np.array([pm0 == None]).any():
        if 'pm0' in par:
            pm0 = par['pm0']
        else:
            pm0 = np.zeros((r, 1))

    pm = c_(pm)
    nna = int(np.max(na)) if na.size > 0 else 0
    nnb = int(np.max(nb)) if nb.size > 0 else 0
    nnc = int(np.max(nc)) if nc.size > 0 else 0
    nni = np.any(pm0)
    z = r * nna + m * nnb + r * nnc + nni
    cnd = r == 1
    if z == 0:
        Pm = np.empty((0, 0))
        return Pm
    Pm = np.zeros((r, z))
    ii = 0
    for i in range(0, r):
        if pm0.size > 0:
            if pm0[i]:
                Pm[i, 0] = pm[int(ii)]
                ii += pm0[i]
        if nna:
            for j in range(0, r):
                Pm[i, nni + j:int(na[i, j]*r - 1 + cnd + j):r] = pm[int(0 + ii):int(na[i, j] + ii), 0]
                ii += na[i, j]
        if nnb:
            for j in range(0, m):
                Pm[i, nni + j + r * nna:int(nb[i, j] * m - 1 + j + r * nna):m] = pm[int(0 + ii):int(nb[i, j] + ii), 0]
                ii += nb[i, j]
        if nnc:
            for j in range(0, r):
                Pm[i, nni + j + r * nna + m * nnb:int(nc[i, j] * r - 1 + cnd + j + r * nna + m * nnb):r] = pm[int(0 + ii):int(
                    nc[i, j] + ii), 0]
                ii += nc[i, j]
    return Pm.T
##############################################################################
# function Y = repmatc(X, m)
# % Columnwise reproduction (m times) of X matrix, i.e. Y = [X X ... X]
# """ USE np.tile """
# def repmatc(X, m):
#     n = X.shape[1]
#     n = size(X,2)
#     Y = X(:, rem(0:(n*m - 1), n) + 1);
#     return Y
##############################################################################
# model_list = roblspm(U, Y, par, opt_dvaf, opt_max_iter, opt_hst)
def roblspm(U, Y, na=0, nb=0, pm0=0, maxiter=50, dvaf=1e-2, hst=0):
    """
    Parameters
    ----------
    U : vector, matrix
        independent variables.
    Y : vector, matrix
        dependent variables.
    par : dict, optional
        DESCRIPTION. The default is {'na':0, 'nb':0, 'pm0':False}.
    opt : dict, optional
        DESCRIPTION. The default is {'maxiter': 100, 'dvaf': 1e-2 , 'hst': 0}.
        maxiter: maximum number of iterations to run
        dvaf: delta in "variance accounted for" statistics * 100; 0% is bad, 100% is good
        hst: whether to keep iteration history in the model object

    Returns
    -------
    return_list : TYPE
        DESCRIPTION.

    """
    N, r = Y.shape
    m = U.shape[1]
    n = max([na, nb])
    F = dmpm(U, Y, na=na, nb=nb, nc=0, pm0=pm0)
    Pm = nsinv(F.T@F)@F.T@Y[n:N][:]
    Ym = F@Pm
    Y1 = Y[n:, :]
    vafw = vaf(Y1, Ym)
    vaf0 = vafw
    if hst:
        VAFw = vafw
        VAF = vaf0
        PM = pm2v(Pm, na=na, nb=nb, pm0=0) # todo: make pm2v() to work for pm0=1
    iter_n = 0
    iterate = 1
    while iterate:
        iter_n += 1
        ww = np.minimum(1, np.maximum(1e-8, 1 / abs(Y1 - Ym)))
        for i in range(r):
            Wi = np.matlib.repmat(c_(ww[:, i]), 1, r * na + m * nb)
            Pm[:, i] = nsinv(F.T@(Wi * F))@F.T@(ww[:, i] * Y1[:, i])
        Ym = F@Pm
        vafw_1 = vafw
        vafw = vaf(Y1, Ym, ww)
        vaf0 = vaf(Y1, Ym)
        if hst:
            PM = np.append(PM, pm2v(Pm, na, nb, pm0=0)) if PM.size > 0 else pm2v(Pm, na, nb, pm0=0)
            VAFw = np.append(VAFw, vafw)
            VAF = np.append(VAF, vaf0)
        iterate = 0 if any(abs(vafw - vafw_1) <= dvaf) or iter_n >= maxiter else 1
    if hst:
        st = {'PM':PM, 'vafw':vafw, 'vaf0':vaf0, 'iterations':iter_n}
    else:
        st = []
    return Pm, st
##############################################################################
def roblspm_apl(U, Y, Pm, na=0, nb=0, pm0=0):
    F = dmpm(U, Y, na=na, nb=nb)
    Ym = F@Pm
    return Ym
##############################################################################
def roblspv(U, Y, na=0, nb=0, pm0=0, maxiter=50, dvaf=1e-2, hst=0):
    N, r = Y.shape
    if len(U) > 0:
        N, m = U.shape
    else:
        m = 0
    if len(Y) > 0:
        N, r = Y.shape
    else:
        r = 0
    if not N > 0:
        print('In ELSPV: At least one data matrix should be not empty...')
        return None
    if isinstance(na, (int, float)):  na = np.full([r, r], na)
    if isinstance(nb, (int, float)):  nb = np.full([r, m], nb)
    if isinstance(pm0, (int, float)): pm0 = np.full([r, 1], pm0)
    n = int(np.max(np.hstack((na, nb))))
    y = vec(Y[n:].T)
    F = dmpv(U, Y, na=na, nb=nb, pm0=pm0)
    pm = nsinv(F.T@F)@F.T@y
    ym = F@pm
    vafw = vaf(dv2dm(y, r), dv2dm(ym, r))
    vaf0 = vafw
    if hst:
        VAFw = vafw
        VAF = vaf0
        PM = pm
        YM = ym
    # -------------------------------------------------------------------    
    iter_n = 0
    iterate = True
    while iterate:
        iter_n += 1
        # print("THIS IS ITERATION ", iter_n)
        w = np.minimum(1, np.maximum(1e-8, abs(y - ym) ** -1))  ## CHECK
        # ww = repmatc(w, size(F, 2)); ## what is repmatC ?
        ww = np.tile(w, F.shape[1])
        # ww and F should have one same dimension:
        pm = np.linalg.inv(F.T@(ww * F))@(ww * F).T@y
        ym = F@pm
        vafw_1 = vafw
        vafw = vaf(dv2dm(y, r), dv2dm(ym, r), dv2dm(w, r))
        vaf0 = vaf(dv2dm(y, r), dv2dm(ym, r))

        if hst:
            PM = np.hstack((PM, pm))
            VAFw = np.hstack((VAFw, vafw))
            VAF = np.hstack((VAF, vaf0))
            YM = np.hstack((YM, ym))
        if any(abs(vafw - vafw_1)) <= dvaf or iter_n >= maxiter:
            iterate = False
    if hst:  # st.
        st = {'PM':PM, 'vafw':vafw, 'vaf0':vaf0, 'iterations':iter_n}
    else:
        st = []
    # ----------------------------------------------------------------
    return pm, st
##############################################################################
# def roblspv_apl():
##############################################################################
