import collections
import collections.abc
import json

import numpy as np
import torch

from ..core.serializable import JSONSerializable
from ..core.utils import process_object, process_objects


class MeanfieldToMultivariate(JSONSerializable, collections.abc.Callable):
    def __init__(
        self, filename, univariate_locations, univariate_scales, location, scale_tril
    ):
        self.filename = filename
        self.univariate_locations = univariate_locations
        self.univariate_scales = univariate_scales
        self.location = location
        self.scale_tril = scale_tril
        self.default_cov = 0.001

    def convert(self):
        with open(self.filename) as fp:
            checkpoint = json.load(fp)
        locs = []
        scales = []

        params = {}
        for param in checkpoint:
            params[param['id']] = param

        for loc in self.univariate_locations:
            if loc.id in params:
                locs.extend(params[loc.id]['tensor'])

        for scale in self.univariate_scales:
            if scale.id in params:
                scales.extend(params[scale.id]['tensor'])

        locs = np.array(locs)
        scales = np.exp(np.array(scales))
        dim = len(locs)
        cov = torch.full((dim, dim), self.default_cov, dtype=torch.float64)
        ind = np.diag_indices(dim)
        cov[ind[0], ind[1]] = torch.tensor(scales) * torch.tensor(scales)
        tril = torch.cholesky(cov)

        indices = torch.tril_indices(row=dim, col=dim, offset=0)

        # we want tril, torchtree does the transform within multivariate_normal
        # should create a transform class for going from 1D tensor to triangular matrix
        # with exponentiation of the diagonal
        self.location.tensor = torch.tensor(locs)
        self.scale_tril.tensor = tril[indices[0], indices[1]]

        self.location.fire_parameter_changed()
        self.scale_tril.fire_parameter_changed()

        # print(locs.tolist())
        # print(tril[indices[0], indices[1]].numpy().tolist())

    def _call(self, *args, **kwargs) -> None:
        self.convert()

    @classmethod
    def from_json(cls, data, dic):
        filename = data['filename']
        univariate_locations = process_objects(data['locations'], dic)
        univariate_scales = process_objects(data['scales'], dic)
        location = process_object(data['location'], dic)
        scale_tril = process_object(data['scale_tril'], dic)
        return cls(
            filename, univariate_locations, univariate_scales, location, scale_tril
        )
