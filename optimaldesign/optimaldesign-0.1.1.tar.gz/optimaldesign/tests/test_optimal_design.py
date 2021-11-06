from optimaldesign.optimal_design import OptimalDesign
import jax.numpy as np
from jax.config import config

config.update("jax_enable_x64", True)


class TestOptimalDesign:
    """
    Test Case with a optimal design for linear regression model with features (1,x,x^2) on
    design space [-1,1] with 101 equal distributed support points as initial grid.
    """

    def quadratic_polynomial(x, c):
        return c[0] + c[1] * x[0] + c[2] * x[0] ** 2

    points_per_dim = 101
    dim = 1
    x_u = np.full(dim, 1)
    x_l = -x_u
    x_q = np.full(dim, points_per_dim, dtype=np.int64)

    optimal_design = OptimalDesign(
        f=quadratic_polynomial, feature_size=3, x_u=x_u, x_l=x_l, x_q=x_q
    )

    def test_solve(self):
        weights, supp = self.optimal_design.solve()
        supp_solution = np.array([[-1], [0], [1]])
        weights_solution = np.array([1 / 3, 1 / 3, 1 / 3])
        assert np.linalg.norm(supp - supp_solution) < 1e-6
        assert np.linalg.norm(weights - weights_solution) < 1e-6
