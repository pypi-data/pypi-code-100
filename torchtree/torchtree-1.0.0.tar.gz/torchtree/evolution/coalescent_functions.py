# import coalescent_cpp
# import torch.autograd
#
# """
# how to use:
# from .coalescent_functions import ConstantCoalescentAutogradFunction
#
#     def log_prob(self, node_heights: torch.Tensor) -> torch.Tensor:
#         fn = ConstantCoalescentAutogradFunction.apply
#         return fn(self.sampling_times, node_heights, self.theta)
# """
#
#
# class ConstantCoalescentAutogradFunction(torch.autograd.Function):
#     @staticmethod
#     def forward(ctx, sampling_times, heights, theta):
#         log_p, indexes = coalescent_cpp.forward(sampling_times, heights, theta)
#         ctx.save_for_backward(indexes, sampling_times, heights, theta)
#         return log_p
#
#     @staticmethod
#     def backward(ctx, grad_output):
#         heights_grad, theta_grad = coalescent_cpp.backward(*ctx.saved_variables)
#         return None, heights_grad * grad_output, theta_grad * grad_output
