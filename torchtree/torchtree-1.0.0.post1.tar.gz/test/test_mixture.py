# import math
# from collections import OrderedDict
#
# import pytest
# import torch
#
# from torchtree import Parameter
# from torchtree.distributions import Distribution
# from torchtree.distributions.mixture import MixtureDistributionModel
#
#
# def test_simple():
#     normal = Distribution(
#         None,
#         torch.distributions.Normal,
#         Parameter(None, torch.tensor([1.0])),
#         OrderedDict(
#             {
#                 'loc': Parameter(None, torch.tensor([0.0])),
#                 'scale': Parameter(None, torch.tensor([1.0])),
#             }
#         ),
#     )
#
#     exp = Distribution(
#         None,
#         torch.distributions.Exponential,
#         Parameter(None, torch.tensor([1.0])),
#         OrderedDict({'rate': Parameter(None, torch.tensor([1.0]))}),
#     )
#     joint = MixtureDistributionModel(
#         None, [normal, exp], Parameter(None, torch.tensor([0.5, 0.5]))
#     )
#     assert (math.exp(-1.418939) * 0.5 - math.exp(1.0) * 0.5) == pytest.approx(
#         joint().item()
#     )
#
#
# def test_mixture_normals():
#     means = torch.tensor([1.0, 2.0])
#     scales = torch.tensor([1.0, 2.0])
#     x = Parameter(None, torch.tensor([1.0, 3.0]))
#     weights = torch.tensor([0.2, 0.8])
#
#     mix = torch.distributions.Categorical(weights)
#     comp = torch.distributions.Normal(means, scales)
#     gmm = torch.distributions.MixtureSameFamily(mix, comp)
#
#     normal1 = Distribution(
#         None,
#         torch.distributions.Normal,
#         x,
#         OrderedDict(
#             {
#                 'loc': Parameter(None, means[:-1]),
#                 'scale': Parameter(None, scales[:-1]),
#             }
#         ),
#     )
#     normal2 = Distribution(
#         None,
#         torch.distributions.Normal,
#         x,
#         OrderedDict(
#             {
#                 'loc': Parameter(None, means[-1:]),
#                 'scale': Parameter(None, scales[-1:]),
#             }
#         ),
#     )
#     joint = MixtureDistributionModel(None, [normal1, normal2], Parameter(None, weights))
#     print(joint())
#     print(gmm.log_prob(x.tensor).sum())
#     assert gmm.log_prob(x.tensor) == pytest.approx(joint().item())
