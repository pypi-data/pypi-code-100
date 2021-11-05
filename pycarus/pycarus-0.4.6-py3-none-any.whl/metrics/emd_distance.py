import os
from importlib.util import find_spec
from typing import Tuple

import torch

from pycarus.geometry.pcd import batchify, unbatchify


def emd(
    prediction: torch.Tensor, groundtruth: torch.Tensor, eps: float, iterations: int, squared: bool
) -> Tuple[torch.Tensor, torch.Tensor]:
    """Compute the Earth Mover's Distance.

    This function uses the auction algorithm for approximation, hence the assignment is not
    guranteed to be a bijection.

    Args:
        prediction: The predicted point cloud with shape ([B,] NUM_POINTS, 3). NUM_POINTS should be
        a multiple of 1024.
        groundtruth: The groundtruth point cloud with shape ([B,] NUM_POINTS, 3). NUM_POINTS should
        be a multiple of 1024.
        eps: the balance between the error rate and the speed of convergence.
        iterations: The max number of iterations.
        squared: If true return the squared euclidean distance.

    Raises:
        ModuleNotFoundError: If the cuda extension is not installed.

    Returns:
        A tuple containing:
        - A tensor with the average computed distance according to Earth Mover's assignment.
        - A tensor with the assigned index for each point.
    """
    if find_spec("emd") is None:
        folder = os.path.dirname(os.path.realpath(__file__))
        str_exp = f"EMD not found. Install it running {folder}/external/setup_emd.py"
        raise ModuleNotFoundError(str_exp)
    else:
        from pycarus.metrics.external.emd_module import EMDDistance  # type: ignore

    batched, [pred, gt] = batchify([prediction, groundtruth], 3)
    emd = EMDDistance()

    distances, assignments = emd(pred, gt, eps, iterations)

    if not squared:
        distances = torch.sqrt(distances)

    distances = distances.mean(1)
    if batched:
        distances, assignments = unbatchify([distances, assignments])

    return distances, assignments
