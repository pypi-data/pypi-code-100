# import copy
#
# import torch
# from torch import nn
#
# from ..distributions.distributions import DistributionModel
#
#
# class LinearMaskedCoupling(nn.Module):
#     """ Modified RealNVP Coupling Layers per the MAF paper """
#
#     def __init__(self, input_size, hidden_size, n_hidden, mask, cond_label_size=None):
#         super().__init__()
#
#         self.register_buffer('mask', mask)
#
#         # scale function
#         s_net = [
#             nn.Linear(
#                 input_size + (cond_label_size if cond_label_size is not None else 0),
#                 hidden_size,
#             )
#         ]
#         for _ in range(n_hidden):
#             s_net += [nn.Tanh(), nn.Linear(hidden_size, hidden_size)]
#         s_net += [nn.Tanh(), nn.Linear(hidden_size, input_size)]
#         self.s_net = nn.Sequential(*s_net)
#
#         # translation function
#         self.t_net = copy.deepcopy(self.s_net)
#         # replace Tanh with ReLU's per MAF paper
#         for i in range(len(self.t_net)):
#             if not isinstance(self.t_net[i], nn.Linear):
#                 self.t_net[i] = nn.ReLU()
#
#     def forward(self, x, y=None):
#         # apply mask
#         mx = x * self.mask
#
#         # run through model
#         s = self.s_net(mx if y is None else torch.cat([y, mx], dim=1))
#         t = self.t_net(mx if y is None else torch.cat([y, mx], dim=1))
#         u = mx + (1 - self.mask) * (x - t) * torch.exp(
#             -s
#         )  # cf RealNVP eq 8 where u corresponds to x (here we're modeling u)
#
#         log_abs_det_jacobian = (
#             -(1 - self.mask) * s
#         )  # log det du/dx; cf RealNVP 8 and 6; note, sum over input_size done at model log_prob
#
#         return u, log_abs_det_jacobian
#
#     def inverse(self, u, y=None):
#         # apply mask
#         mu = u * self.mask
#
#         # run through model
#         s = self.s_net(mu if y is None else torch.cat([y, mu], dim=1))
#         t = self.t_net(mu if y is None else torch.cat([y, mu], dim=1))
#         x = mu + (1 - self.mask) * (u * s.exp() + t)  # cf RealNVP eq 7
#
#         log_abs_det_jacobian = (1 - self.mask) * s  # log det dx/du
#
#         return x, log_abs_det_jacobian
#
#
# class BatchNorm(nn.Module):
#     """ RealNVP BatchNorm layer """
#
#     def __init__(self, input_size, momentum=0.9, eps=1e-5):
#         super().__init__()
#         self.momentum = momentum
#         self.eps = eps
#
#         self.log_gamma = nn.Parameter(torch.zeros(input_size))
#         self.beta = nn.Parameter(torch.zeros(input_size))
#
#         self.register_buffer('running_mean', torch.zeros(input_size))
#         self.register_buffer('running_var', torch.ones(input_size))
#
#     def forward(self, x, cond_y=None):
#         if self.training:
#             self.batch_mean = x.mean(0)
#             self.batch_var = x.var(
#                 0
#             )  # note MAF paper uses biased variance estimate; ie x.var(0, unbiased=False)
#
#             # update running mean
#             self.running_mean.mul_(self.momentum).add_(
#                 self.batch_mean.data * (1 - self.momentum)
#             )
#             self.running_var.mul_(self.momentum).add_(
#                 self.batch_var.data * (1 - self.momentum)
#             )
#
#             mean = self.batch_mean
#             var = self.batch_var
#         else:
#             mean = self.running_mean
#             var = self.running_var
#
#         # compute normalized input (cf original batch norm paper algo 1)
#         x_hat = (x - mean) / torch.sqrt(var + self.eps)
#         y = self.log_gamma.exp() * x_hat + self.beta
#
#         # compute log_abs_det_jacobian (cf RealNVP paper)
#         log_abs_det_jacobian = self.log_gamma - 0.5 * torch.log(var + self.eps)
#         #        print('in sum log var {:6.3f} ; out sum log var {:6.3f}; sum log det {:8.3f}; mean log_gamma {:5.3f}; mean beta {:5.3f}'.format(
#         #            (var + self.eps).log().sum().data.numpy(), y.var(0).log().sum().data.numpy(), log_abs_det_jacobian.mean(0).item(), self.log_gamma.mean(), self.beta.mean()))
#         return y, log_abs_det_jacobian.expand_as(x)
#
#     def inverse(self, y, cond_y=None):
#         if self.training:
#             mean = self.batch_mean
#             var = self.batch_var
#         else:
#             mean = self.running_mean
#             var = self.running_var
#
#         x_hat = (y - self.beta) * torch.exp(-self.log_gamma)
#         x = x_hat * torch.sqrt(var + self.eps) + mean
#
#         log_abs_det_jacobian = 0.5 * torch.log(var + self.eps) - self.log_gamma
#
#         return x, log_abs_det_jacobian.expand_as(x)
#
#
# class RealNVP(nn.Module):
#     def __init__(
#         self,
#         n_blocks,
#         input_size,
#         hidden_size,
#         n_hidden,
#         cond_label_size=None,
#         batch_norm=True,
#     ):
#         super().__init__()
#
#         # base distribution for calculation of log prob under the model
#         self.register_buffer('base_dist_mean', torch.zeros(input_size))
#         self.register_buffer('base_dist_var', torch.ones(input_size))
#
#         # construct model
#         modules = []
#         mask = torch.arange(input_size).float() % 2
#         for i in range(n_blocks):
#             modules += [
#                 LinearMaskedCoupling(
#                     input_size, hidden_size, n_hidden, mask, cond_label_size
#                 )
#             ]
#             mask = 1 - mask
#             modules += batch_norm * [BatchNorm(input_size)]
#
#         self.net = FlowSequential(*modules)
#
#     @property
#     def base_dist(self):
#         return D.Normal(self.base_dist_mean, self.base_dist_var)
#
#     def forward(self, x, y=None):
#         return self.net(x, y)
#
#     def inverse(self, u, y=None):
#         return self.net.inverse(u, y)
#
#     def log_prob(self, x, y=None):
#         u, sum_log_abs_det_jacobians = self.forward(x, y)
#         return torch.sum(self.base_dist.log_prob(u) + sum_log_abs_det_jacobians, dim=1)
#
#
# class RealNVP(DistributionModel):
#     """
#     Class for normalizing flows.
#
#     :param id_: ID of object
#     :param x: parameter or list of parameters
#     :param base: base distribution
#     :param modules: list of transformations
#     """
#
#     def __init__(
#         self,
#         id_: str,
#         x: Union[Parameter, List[Parameter]],
#         base: Distribution,
#         modules: List[Module],
#     ) -> None:
#         DistributionModel.__init__(self, id_)
#         self.x = x
#         self.base = base
#         self.modules = modules
#         self.layers = nn.ModuleList([t.module for t in modules])
#         self.sum_log_abs_det_jacobians = None
#
#         # construct model
#         modules = []
#         mask = torch.arange(input_size).float() % 2
#         for i in range(n_blocks):
#             modules += [
#                 LinearMaskedCoupling(
#                     input_size, hidden_size, n_hidden, mask, cond_label_size
#                 )
#             ]
#             mask = 1 - mask
#             modules += batch_norm * [BatchNorm(input_size)]
#
#         self.net = FlowSequential(*modules)
#
#     def forward(self, x: Tensor) -> Tuple[Tensor, Tensor]:
#         log_det_J = 0.0
#         z = x
#         for layer in self.layers:
#             y = layer(z)
#             log_det_J += layer.log_abs_det_jacobian(y, z)
#             z = y
#         return z, log_det_J
#
#     def apply_flow(self, sample_shape: Size):
#         if sample_shape == torch.Size([]):
#             zz, self.sum_log_abs_det_jacobians = self.forward(
#                 self.base.field.tensor.unsqueeze(0)
#             )
#             zz = zz.squeeze()
#         else:
#             zz, self.sum_log_abs_det_jacobians = self.forward(self.base.field.tensor)
#
#         if isinstance(self.x, (list, tuple)):
#             offset = 0
#             for xx in self.x:
#                 xx.tensor = zz[..., offset : (offset + xx.shape[-1])]
#                 offset += xx.shape[-1]
#         else:
#             self.x.tensor = zz
#
#     def sample(self, sample_shape=Size()) -> None:
#         self.base.sample(sample_shape)
#         self.apply_flow(sample_shape)
#
#     def rsample(self, sample_shape=Size()) -> None:
#         self.base.rsample(sample_shape)
#         self.apply_flow(sample_shape)
#
#     def log_prob(self, x: Union[List[Parameter], Parameter] = None) -> Tensor:
#         return self.base() - self.sum_log_abs_det_jacobians
#
#     def _call(self, *args, **kwargs) -> Tensor:
#         return self.log_prob()
#
#     @property
#     def batch_shape(self) -> torch.Size:
#         return self.base.batch_shape
#
#     @property
#     def sample_shape(self) -> torch.Size:
#         return self.base.sample_shape
#
#     def parameters(self) -> List[Parameter]:
#         parameters = []
#         for module in self.modules:
#             parameters.extend(module.parameters())
#         return parameters
#
#     def handle_model_changed(self, model, obj, index):
#         pass
#
#     def handle_parameter_changed(self, variable, index, event):
#         pass
#
#     @classmethod
#     def from_json(cls, data: Dict[str, any], dic: Dict[str, any]) -> 'NormalizingFlow':
#         id_ = data['id']
#         x = process_objects(data['x'], dic)
#         base = process_object(data['base'], dic)
#         modules = process_objects(data['layers'], dic)
#
#         return cls(id_, x, base, modules)
