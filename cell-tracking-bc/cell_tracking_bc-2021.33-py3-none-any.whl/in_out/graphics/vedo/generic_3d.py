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

from typing import Optional, Sequence

import numpy as nmpy
from vedo import Picture as picture_t
from vedo import Plotter as axes_3d_t
from vedo import Volume as volume_t
from vedo.shapes import Text3D as text_t

from cell_tracking_BC.type.frame import frame_t
from cell_tracking_BC.type.tracks import tracks_t


array_t = nmpy.ndarray


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
    kept_frames = frames[::keep_every]

    min_intensity = min(nmpy.amin(_frm) for _frm in kept_frames)
    max_intensity = max(nmpy.amax(_frm) for _frm in kept_frames)
    intensity_range = max(1, max_intensity - min_intensity)

    size = 0.5 * sum(kept_frames[0].shape)
    time_scaling = 0.3 * size
    for t_idx, frame in enumerate(kept_frames):
        height = time_scaling * t_idx

        scaled = 255.0 * (frame - min_intensity) / intensity_range
        picture = picture_t(scaled).z(height).alpha(0.8)
        axes += picture

        if (cell_contours is not None) or with_cell_labels or (tracks is not None):
            # if cell_contours is None:
            #     contours = None
            # else:
            #     contours = cell_contours[t_idx]
            if cell_frames is None:
                cells = []
            else:
                cells = cell_frames[t_idx].cells

            for cell in cells:
                position = [
                    cell.centroid[1],
                    cell.centroid[0],
                    height + 0.1 * time_scaling,
                ]
                text = []
                if with_cell_labels:
                    text.append(str(cell.label))
                else:
                    text.append("")
                if tracks is None:
                    text.append("")
                else:
                    labels = tracks.TrackLabelsContainingCell(cell)
                    if labels is None:
                        text.append("?")
                    else:
                        if labels.__len__() > 1:
                            labels = "\n".join(str(_lbl) for _lbl in labels)
                        else:
                            labels = str(labels[0])
                        text.append(labels)
                text = ",".join(text)
                text = text_t(text, position, s=8, depth=1, justify="centered", c="red")
                text.alpha(0.95)
                text.followCamera()
                axes += text


def ShowFramesAsTunnels(
    frames: Sequence[array_t],
    axes: axes_3d_t,
    /,
    *,
    keep_every: int = 2,
    iso_value: float = 0.5,
) -> None:
    """"""
    kept_frames = frames[::keep_every]

    size = 0.5 * sum(kept_frames[0].shape)
    time_scaling = 0.3 * size

    volume = nmpy.array(kept_frames, dtype=nmpy.uint8)
    isosurface = volume_t(volume).isosurface([iso_value])
    isosurface.scale(s=(1.0, 1.0, time_scaling))
    axes += isosurface
