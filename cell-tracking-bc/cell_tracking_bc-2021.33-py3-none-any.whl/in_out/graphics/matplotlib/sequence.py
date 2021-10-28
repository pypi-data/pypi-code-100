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

from typing import Optional, Sequence, Union

import matplotlib.pyplot as pypl
import numpy as nmpy

import cell_tracking_BC.in_out.graphics.matplotlib.generic as gphc
import cell_tracking_BC.in_out.graphics.matplotlib.generic_2d as gph2
import cell_tracking_BC.in_out.graphics.matplotlib.generic_3d as gph3
from cell_tracking_BC.in_out.file.archiver import archiver_t
from cell_tracking_BC.in_out.graphics.matplotlib.generic_2d import sequence_2D_t
from cell_tracking_BC.type.sequence import sequence_t


array_t = nmpy.ndarray


def ShowSequenceStatistics(
    sequence: sequence_t,
    /,
    *,
    channel: Union[str, Sequence[str]] = None,
    show_and_wait: bool = True,
    figure_name: str = "sequence-statistics",
    archiver: archiver_t = None,
) -> None:
    """"""
    if channel is None:
        channels = sequence.base_channels
    elif isinstance(channel, str):
        channels = (channel,)
    else:
        channels = channel

    statistics = ("amin", "amax", "mean", "median")
    ComputedStatistics = tuple(getattr(nmpy, _stt) for _stt in statistics)
    records = {_stt: {_chl: [] for _chl in channels} for _stt in statistics}
    for frames in sequence.Frames(channel=channels):
        for channel, frame in zip(channels, frames):
            for name, Computed in zip(statistics, ComputedStatistics):
                records[name][channel].append(Computed(frame))

    figure, all_axes = pypl.subplots(nrows=statistics.__len__())

    for s_idx, (name, values_per_channel) in enumerate(records.items()):
        for channel, values in values_per_channel.items():
            all_axes[s_idx].plot(values, label=channel)

    for name, axes in zip(records.keys(), all_axes):
        gph2.SetTimeAxisProperties(sequence.length - 1, axes)
        axes.legend()
        axes.set_title(name)

    gphc.FinalizeDisplay(figure, figure_name, show_and_wait, archiver)


def ShowSequence(
    sequence: Union[Sequence[array_t], sequence_t],
    /,
    *,
    channel: str = None,
    with_segmentation: bool = True,
    with_cell_labels: bool = True,
    with_track_labels: bool = True,
    mode: str = "2d+t",
    keep_every: int = 2,
    n_levels: int = 100,
    iso_value: float = None,
    with_ticks: bool = True,
    with_colorbar: bool = True,
    show_and_wait: bool = True,
    figure_name: str = "sequence",
    archiver: archiver_t = None,
) -> Optional[Union[pypl.Figure, sequence_2D_t]]:
    """
    mode: "2d+t", "mille-feuille", "tunnels"
    """
    output = None

    if mode == "2d+t":
        viewer = sequence_2D_t.NewForChannels(
            sequence,
            channel=channel,
            with_segmentation=with_segmentation,
            with_cell_labels=with_cell_labels,
            with_track_labels=with_track_labels,
            with_ticks=with_ticks,
            with_colorbar=with_colorbar,
            figure_name=figure_name,
            archiver=archiver,
        )
        if show_and_wait:
            pypl.show()
        else:
            output = viewer
    elif mode in ("mille-feuille", "tunnels"):
        if isinstance(sequence, sequence_t):
            if channel is None:
                channel = sequence.cell_channel
            frames = sequence.Frames(channel=channel)
        else:
            frames = sequence

        figure, axes = gph3.FigureAndAxes()
        if mode == "mille-feuille":
            if isinstance(sequence, sequence_t) and sequence.has_cells:
                cell_frames = sequence.cell_frames
            else:
                cell_frames = None
            cell_contours = gphc.CellContours(sequence, with_segmentation)
            tracks = gphc.CellTracks(sequence, with_track_labels)
            gph3.ShowFramesAsMilleFeuille(
                frames,
                cell_contours,
                with_cell_labels,
                cell_frames,
                tracks,
                axes,
                keep_every=keep_every,
                n_levels=n_levels,
            )
        else:
            if iso_value is None:
                iso_value = nmpy.median(frames[0])
            gph3.ShowFramesAsTunnels(
                frames, axes, keep_every=keep_every, iso_value=iso_value
            )

        if not show_and_wait:
            output = figure
        gphc.FinalizeDisplay(figure, figure_name, show_and_wait, archiver)
    else:
        raise ValueError(
            f'{mode}: Invalid mode; Expected="2d+t", "mille-feuille", "tunnels"'
        )

    return output
