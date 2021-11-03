import numpy as np
import solvers.wcvxopt as ilp

def test_solve_simple_ilp():

    status, solution = ilp.solve_boolean_lp(
        obj=np.array([1,2,3]),
        aub=np.array([
            [-1,1,0],
            [0,0,1],
        ]),
        bub=np.array([0,1]),
        minimize=True,
    )
    assert status == 'optimal'
    assert solution.tolist() == [0,0,1]