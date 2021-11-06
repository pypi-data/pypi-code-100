from optimaldesign.interior_point_method import FunctionTarget
import jax.numpy as np
import jax.scipy as sp
from jax import jit
from functools import partial


class DCritWeights(FunctionTarget):
    def set_constants(self, linear_model, supp):
        self.linear_model = linear_model
        self.design = linear_model.design(supp)
        self.supp = supp

    @partial(jit, static_argnums=(0,))
    def compute(self, weights):
        fim = self.linear_model.fim(weights, self.supp)
        phi = np.dot(
            self.design,
            sp.linalg.lu_solve(sp.linalg.lu_factor(fim), self.design.T),
        )
        det = np.linalg.det(fim)
        value = -np.log(det)
        gradient = -np.diag(phi)
        hessian = phi ** 2
        return value, gradient, hessian


class DCritSupp(FunctionTarget):
    def set_constants(self, linear_model, weights, supp):
        self.linear_model = linear_model
        self.fim = linear_model.fim(weights, supp)

    @partial(jit, static_argnums=(0,), backend="cpu")
    def compute(self, x):
        feature_vec = self.linear_model.feature_vec(x)
        inv_fim_design = sp.linalg.lu_solve(sp.linalg.lu_factor(self.fim), feature_vec)
        jac = self.linear_model.jac(x)
        # vec_hessian = self.linear_model.feature_vec_hessian(x)
        result_value = (
            -np.dot(feature_vec, inv_fim_design) + self.linear_model.feature_size
        )
        result_gradient = -np.dot(jac.T, inv_fim_design)
        # return (result_value, result_gradient, 0)
        # result_hessian = -np.dot(
        #     jac.T,
        #     sp.linalg.lu_solve(
        #         sp.linalg.lu_factor(self.fim),
        #         jac,
        #     ),
        # )
        # for i in range(x.shape[0]):
        #     for j in range(x.shape[0]):
        #         result_hessian = ops.index_update(
        #             result_hessian,
        #             ops.index[i, j],
        #             result_hessian[i, j] - np.dot(vec_hessian[:, i, j], inv_fim_design),
        #         )

        return result_value, result_gradient, 0


# class CCritWeights(FunctionTarget):
#     def set_constants(self, linear_model, supp, m):
#         self.linear_model = linear_model
#         self.design = linear_model.design(supp)
#         self.supp = supp
#         self.m = m

#     @partial(jit, static_argnums=(0,))
#     def compute(self, weights):
#         feat_size = self.linear_model.selected_feature_size
#         fim = self.linear_model.fim(weights, self.supp)

#         e_n = np.ones_like(feat_size)
#         e_n = ops.index_update(e_n, ops.index[feat_size - self.m :], 0)

#         return value, gradient, hessian
