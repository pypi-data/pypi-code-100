import numpy as np
import cvxopt
import cvxopt.glpk
from utils.redirector import redirect_stdout2devnull


cvxopt.glpk.options["msg_lev"] = "GLP_MSG_OFF"


def solve_boolean_lp(
    obj: np.ndarray,
    aub: np.ndarray,
    bub: np.ndarray,
    aeq: np.ndarray=None,
    beq: np.ndarray=None,
    minimize: bool=True):
    """
        Solve a BLP (boolean linear programming) problem of the type

        Min obj * x           or    Max obj * x
        s.t. aub * x ≥ bub          s.t. aub * x ≥ bub
             aeq * x = beq               aeq * x = beq
        (^default)

        Parameters
        obj: The objective function coefficients as an ndarray with shape (n,)
        aub: Constraint matrix as an ndarray with shape (m, n)
        bub: Support vector as an ndarray with shape (m,)
        aeq: Constraint matrix as an ndarray with shape (p, n)
        beq: Support vector as an ndarray with shape (p,)
        minimize: If True use the minimization BLP, otherwise use maximization BLP

        Returns
        status: The status returned by the GLPK ILP solver (see help(cvxopt.glpk.ilp) for info)
        x: If the status is 'optimal', 'feasible' or 'undefined' then this will be a solution vector as an ndarray
    """

    if len(obj.shape) != 1:
        raise ValueError("'obj' must be a one-dimensional array of shape: (n,)")

    dim = obj.shape[0]

    def validate_constraint_format(mat: np.ndarray, sup: np.ndarray) -> bool:
        if (mat is not None) or (sup is not None):
            if not (isinstance(mat, np.ndarray) and isinstance(sup, np.ndarray)):
                return False

            if len(mat.shape) != 2 or len(sup.shape) != 1:
                return False

            if mat.shape[1] != dim or mat.shape[0] != sup.shape[0]:
                return False
        return True

    if not validate_constraint_format(aub, bub):
        raise ValueError("'aub' must be a two-dimensional ndarray of shape (m, n) and 'bub' must be a one-dimensional ndarray of shape (m,) where n is the length of 'obj'")
    if not validate_constraint_format(aeq, beq):
        raise ValueError("'aeq' must be a two-dimensional ndarray of shape (m, n) and 'beq' must be a one-dimensional ndarray of shape (m,) where n is the length of 'obj'")

    if minimize:
        # Minimize (default)
        c = cvxopt.matrix(obj.astype(np.float).tolist())
    else:
        # Maximize -> swap sign on the objective
        c = cvxopt.matrix((obj * -1).astype(np.float).tolist())

    # Constraint format is >=
    # Swap sign on coefficients in constraint matrix and support vector
    G = cvxopt.matrix((aub * -1).astype(np.float).T.tolist()) if not aub is None else None
    h = cvxopt.matrix((bub * -1).astype(np.float).tolist()) if not bub is None else None

    A = cvxopt.matrix(aeq.astype(np.float).T.tolist()) if not aeq is None else None
    b = cvxopt.matrix(beq.astype(np.float).tolist()) if not beq is None else None
    I = set()  # No variables should be integer ...
    B = set(i for i in range(dim))  # ... all should be boolean (0 or 1)

    with redirect_stdout2devnull():
        status, x = cvxopt.glpk.ilp(c, G, h, A, b, I, B)

    if status in ['optimal', 'feasible', 'undefined']:
        x = np.array(x).flatten().astype(np.int16)

    return (status, x)

async def ilp_solver_wrapper(ilp_problems: list) -> list:
    return [(k, solve_boolean_lp(**problem)) for (k, problem) in ilp_problems]