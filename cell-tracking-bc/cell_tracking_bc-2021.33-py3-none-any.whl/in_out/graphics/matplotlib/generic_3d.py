# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2021)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

from __future__ import annotations

from typing import Optional, Sequence, Tuple

import matplotlib.pyplot as pypl
import numpy as nmpy
import scipy.interpolate as ntrp
import skimage.measure as msre
from mpl_toolkits.mplot3d import Axes3D as axes_3d_t

from cell_tracking_BC.in_out.graphics.matplotlib.generic import AnnotateCells
from cell_tracking_BC.type.frame import frame_t
from cell_tracking_BC.type.tracks import tracks_t


array_t = nmpy.ndarray


_MC_STEP_SIZE = 5  # MC=marching cubes
_MIN_MC_TIME_STEPS = 3


def ShowFramesAsMilleFeuille(
    frames: Sequence[array_t],
    cell_contours: Optional[Sequence[Sequence[array_t]]],
    with_cell_labels: bool,
    cell_frames: Optional[Sequence[frame_t]],
    tracks: Optional[tracks_t],
    axes: axes_3d_t,
    /,
    *,
    keep_every: int = 2,
    n_levels: int = 1,
) -> None:
    """"""
    n_frames = frames.__len__()
    shape = frames[0].shape

    all_rows, all_cols = nmpy.meshgrid(range(shape[0]), range(shape[1]), indexing="ij")
    for t_idx, frame in enumerate(frames):
        if t_idx % keep_every > 0:
            continue

        axes.contourf(
            all_rows,
            all_cols,
            frame,
            levels=n_levels,
            offset=t_idx,
            alpha=0.8,
            cmap="gray",
        )
        if (cell_contours is not None) or with_cell_labels or (tracks is not None):
            if cell_contours is None:
                contours = None
            else:
                contours = cell_contours[t_idx]
            if cell_frames is None:
                cell_frame = None
            else:
                cell_frame = cell_frames[t_idx]

            _ = AnnotateCells(
                frame,
                contours,
                with_cell_labels,
                cell_frame,
                tracks,
                axes,
                elevation=t_idx + 0.2,
            )

    SetZAxisProperties(n_frames - 1, axes)


def ShowFramesAsTunnels(
    frames: Sequence[array_t],
    axes: axes_3d_t,
    /,
    *,
    keep_every: int = 2,
    iso_value: float = 0.5,
) -> None:
    """"""
    volume = nmpy.array(frames, dtype=nmpy.uint8)
    n_frames_all = frames.__len__()
    n_frames_kept = int((n_frames_all - 1) / keep_every) + 1
    frame_shape = volume.shape[1:]

    original_extents = (
        range(n_frames_all),
        range(frame_shape[0]),
        range(frame_shape[1]),
    )
    interpolated_extents = (
        nmpy.linspace(
            0, n_frames_all - ((n_frames_all - 1) % keep_every) - 1, num=n_frames_kept
        ),
        *original_extents[1:],
    )
    all_times, all_rows, all_cols = nmpy.meshgrid(*interpolated_extents, indexing="ij")
    interpolated_sites = nmpy.vstack((all_times.flat, all_rows.flat, all_cols.flat)).T
    interpolated = ntrp.interpn(original_extents, volume, interpolated_sites)

    reshaped = nmpy.reshape(interpolated, (n_frames_kept, *frame_shape))
    reorganized = nmpy.moveaxis(reshaped, (0, 1, 2), (2, 0, 1))
    flipped = nmpy.flip(reorganized, axis=2)

    if n_frames_kept / _MC_STEP_SIZE < _MIN_MC_TIME_STEPS:
        step_size = max(1, int(round(n_frames_kept / _MIN_MC_TIME_STEPS)))
    else:
        step_size = _MC_STEP_SIZE
    try:
        vertices, faces, *_ = msre.marching_cubes(
            flipped, iso_value, step_size=step_size
        )
    except RuntimeError as exception:
        print(
            f"{ShowFramesAsTunnels.__name__}: Error in {iso_value}-isosurface extraction "
            f"in volume with min {nmpy.amin(flipped)} and max {nmpy.amax(flipped)} "
            f"with step size {step_size}\n{exception}"
        )
        return

    vertices[:, 2] *= keep_every
    axes.plot_trisurf(
        vertices[:, 0],
        vertices[:, 1],
        faces,
        nmpy.amax(vertices[:, 2]) - vertices[:, 2],
        cmap="rainbow",
        lw=1,
    )
    SetZAxisProperties(n_frames_all - 1, axes)


def FigureAndAxes() -> Tuple[pypl.Figure, axes_3d_t]:
    """"""
    figure = pypl.figure()
    axes = figure.add_subplot(projection=axes_3d_t.name)
    axes.set_xlabel("row positions")
    axes.set_ylabel("column positions")
    axes.set_zlabel("time points")

    return figure, axes


def SetZAxisProperties(z_max: int, axes: axes_3d_t, /) -> None:
    """"""
    axes.set_zlim(0, z_max)

    n_ticks = min(20, z_max + 1)
    axes.set_zticks(nmpy.linspace(0.0, z_max, num=n_ticks))
    axes.set_zticklabels(
        str(round(z_max * _idx / (n_ticks - 1), 1)) for _idx in range(n_ticks)
    )
