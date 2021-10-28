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

import dataclasses as dtcl
import warnings as wrng
from sys import maxsize as MAX_INTEGER
from typing import List, Optional, Sequence, Tuple

import matplotlib.pyplot as pypl
import networkx as grph
import numpy as nmpy
from matplotlib import cm as colormap_t
from matplotlib.backend_bases import MouseEvent as mouse_event_t
from matplotlib.collections import PathCollection as path_collection_t
from matplotlib.colors import LinearSegmentedColormap as linear_colormap_t
from matplotlib.text import Annotation as annotation_t

from cell_tracking_BC.in_out.file.archiver import archiver_t
from cell_tracking_BC.in_out.graphics.matplotlib.generic import FinalizeDisplay
from cell_tracking_BC.in_out.graphics.matplotlib.generic_2d import sequence_2D_t
from cell_tracking_BC.in_out.graphics.matplotlib.generic_3d import FigureAndAxes
from cell_tracking_BC.in_out.graphics.tree_layout import ForkingVersionForLayout
from cell_tracking_BC.type.sequence import sequence_t
from cell_tracking_BC.type.track import (
    forking_track_t,
    single_track_t,
)


axes_2d_t = pypl.Axes


_LOW_AFFINITY = 0.75
_MATPLOTLIB_COLORS = ("b", "g", "r", "c", "m", "y", "k")


@dtcl.dataclass(repr=False, eq=False)
class tracking_2D_t:

    figure: pypl.Figure
    axes_track: axes_2d_t
    colormap: colormap_t
    viewer: sequence_2D_t

    scatter: path_collection_t = dtcl.field(init=False, default=None)
    annotation: annotation_t = dtcl.field(init=False, default=None)

    # Cell details
    labels: List[int] = dtcl.field(init=False, default_factory=list)
    time_points: List[int] = dtcl.field(init=False, default_factory=list)
    affinities: List[float] = dtcl.field(init=False, default_factory=list)
    colors: List[int] = dtcl.field(init=False, default_factory=list)

    @classmethod
    def NewForSequence(
        cls,
        sequence: sequence_t,
        /,
        *,
        figure_name: str = "tracking 2D",
        archiver: archiver_t = None,
    ) -> tracking_2D_t:
        """
        Annotation-on-hover code adapted from:
        https://stackoverflow.com/questions/7908636/how-to-add-hovering-annotations-in-matplotlib
        Answered by ImportanceOfBeingErnest on Nov 7 '17 at 20:23
        Edited by waterproof on Aug 12 '19 at 20:08
        """
        figure = pypl.figure()
        two_axes = figure.subplots(1, 2)

        axes_track = two_axes[0]
        axes_track.set_xlabel("time points")
        axes_track.set_ylabel("tracks")
        axes_track.yaxis.set_label_position("right")
        axes_track.yaxis.tick_right()
        axes_track.yaxis.set_ticks(
            range(1, sum(_tck.n_leaves for _tck in sequence.tracks) + 1)
        )

        colormap = colormap_t.get_cmap("plasma")
        mappable = colormap_t.ScalarMappable(cmap=colormap)
        figure.colorbar(mappable, ax=axes_track, location="left")

        viewer = sequence_2D_t.NewForAllStreams(
            sequence,
            with_segmentation=True,
            with_cell_labels=True,
            with_track_labels=True,
            in_axes=two_axes[1],
        )

        instance = cls(
            figure=figure,
            axes_track=axes_track,
            colormap=colormap,
            viewer=viewer,
        )

        all_cell_heights = []
        all_tracks = list(sequence.tracks)
        for which in ("single", "forking"):
            if (tracks := sequence.invalid_tracks[which]) is not None:
                all_tracks.extend(tracks)
        tick_details = []
        n_valid = sequence.tracks.__len__()
        for t_idx, track in enumerate(all_tracks):
            if isinstance(track, single_track_t):
                PlotTrackEdges = instance._PlotSingleTrackEdges
            else:
                PlotTrackEdges = instance._PlotForkingTrackEdges
            new_labels = PlotTrackEdges(track, all_cell_heights, t_idx < n_valid)
            tick_details.extend(new_labels)

        scatter = axes_track.scatter(
            instance.time_points,
            all_cell_heights,
            marker="o",
            c=instance.colors,
            zorder=2,
        )
        positions, labels = zip(*tick_details)
        axes_track.yaxis.set_ticks(positions)
        axes_track.yaxis.set_ticklabels(labels)
        annotation = axes_track.annotate(
            "",
            xy=(0, 0),
            xytext=(20, 20),
            textcoords="offset points",
            bbox={"boxstyle": "round", "fc": "c"},
            arrowprops={"arrowstyle": "-"},
        )
        annotation.set_visible(False)

        instance.scatter = scatter
        instance.annotation = annotation

        figure.canvas.mpl_connect("button_press_event", instance._OnButtonPress)

        figure.tight_layout(h_pad=0.05)
        FinalizeDisplay(figure, figure_name, False, archiver)

        return instance

    def _PlotSingleTrackEdges(
        self,
        track: single_track_t,
        all_cell_heights: List[int],
        is_valid: bool,
        /,
    ) -> Sequence[Tuple[float, int]]:
        """"""
        length, time_points, label, where = self._ElementsForTrackPieces(track)

        self.labels.insert(where, track.root.label)
        self.time_points.insert(where, track.root_time_point)
        self.affinities.insert(where, 0.0)
        self.colors.insert(where, self.colormap(0.0))

        heights = (length + 1) * (label,)
        all_cell_heights.extend(heights)

        if is_valid:
            color = "gray"
        else:
            color = "red"
        self.axes_track.plot(time_points, heights, color=color, zorder=1)

        return ((label, label),)

    def _PlotForkingTrackEdges(
        self,
        track: forking_track_t,
        all_cell_heights: List[int],
        is_valid: bool,
        /,
    ) -> Sequence[Tuple[float, int]]:
        """"""
        with_int_labels, integer_to_cell = ForkingVersionForLayout(track)
        try:
            int_layout = grph.nx_agraph.pygraphviz_layout(with_int_labels, prog="dot")
        except Exception as exc:
            wrng.warn(f"Track layout failed for {track} with error:\n{exc}")
            return ()
        positions = {
            integer_to_cell[_idx]: _pst
            for _idx, _pst in int_layout.items()
            if isinstance(_idx, int)
        }

        output = []

        all_time_points, all_heights = [], []
        min_height = max_height = positions[track.root][0]
        min_label = MAX_INTEGER
        root_height = None
        where = None
        for piece in track.Pieces():
            _, time_points, label, new_where = self._ElementsForTrackPieces(piece)
            heights = nmpy.fromiter(
                (positions[_cll][0] for _cll in piece), dtype=nmpy.float64
            )
            if piece[0] is track.root:
                root_height = heights[0]
            if where is None:
                where = new_where

            all_time_points.append(time_points)
            all_heights.append(heights)
            min_height = min(min_height, min(heights))
            max_height = max(max_height, max(heights))
            if label is not None:
                if label < min_label:
                    min_label = label
                output.append((heights[-1], label))

        height_scaling = (track.n_leaves - 1) / (max_height - min_height)
        AdjustedHeight = lambda _hgt: height_scaling * (_hgt - min_height) + min_label

        output = tuple((AdjustedHeight(_elm[0]), _elm[1]) for _elm in sorted(output))

        if is_valid:
            color = "gray"
        else:
            color = "red"
        for time_points, heights in zip(all_time_points, all_heights):
            heights = AdjustedHeight(heights)
            self.axes_track.plot(time_points, heights, color=color, zorder=1)
            all_cell_heights.extend(heights[1:])
        root_height = AdjustedHeight(root_height)

        self.labels.insert(where, track.root.label)
        self.time_points.insert(where, track.root_time_point)
        self.affinities.insert(where, 0.0)
        self.colors.insert(where, self.colormap(0.0))

        all_cell_heights.insert(where, root_height)

        return output

    def _ElementsForTrackPieces(
        self,
        track: single_track_t,
        /,
    ) -> Tuple[int, Sequence[int], Optional[int], int]:
        """"""
        where = self.labels.__len__()

        root_time_point = track.root_time_point
        length = track.length
        label = track.label
        affinities = track.affinities

        time_points = tuple(range(root_time_point, root_time_point + length + 1))
        colors = tuple(self.colormap(_ffy) for _ffy in affinities)

        self.labels.extend(_cll.label for _cll in track[1:])
        self.time_points.extend(time_points[1:])
        self.affinities.extend(affinities)
        self.colors.extend(colors)

        return length, time_points, label, where

    def _OnButtonPress(
        self,
        event: mouse_event_t,
        /,
    ) -> None:
        """"""
        if event.inaxes is self.axes_track:
            self._ShowAnnotation(event)
        elif event.inaxes is self.viewer.axes:
            pass
        elif self.annotation.get_visible():
            self.annotation.set_visible(False)
            self.figure.canvas.draw_idle()

    def _ShowAnnotation(
        self,
        event: mouse_event_t,
        /,
    ) -> None:
        """"""
        inside, details = self.scatter.contains(event)
        if inside:
            idx = details["ind"][0]
            time_point = self.time_points[idx]
            label = self.labels[idx]

            position = self.scatter.get_offsets()[idx]
            text = f"Time {time_point}\nCell {label}\nPJcd {self.affinities[idx]:.2f}"
            self.annotation.xy = position
            self.annotation.set_text(text)
            self.annotation.set_visible(True)

            self.viewer.ShowFrame(time_point=time_point, highlighted=label)

    def ShowAndWait(self) -> None:
        """"""
        pypl.show()


def ShowTracking3D(
    sequence: sequence_t,
    /,
    *,
    with_track_labels: bool = True,
    with_cell_labels: bool = True,
    show_and_wait: bool = True,
    figure_name: str = "tracking 3D",
    archiver: archiver_t = None,
) -> None:
    """"""
    figure, axes = FigureAndAxes()
    colormap = linear_colormap_t.from_list(
        "affinity", ((0.0, "k"), (0.75, "r"), (1.0, "b"))
    )

    for t_idx, track in enumerate(sequence.tracks):
        low_affinities = tuple(_ffn < _LOW_AFFINITY for _ffn in track.affinities)
        low_fraction = nmpy.count_nonzero(low_affinities) / (
            0.3 * low_affinities.__len__()
        )
        color = colormap(1.0 - min(1.0, low_fraction))

        for piece in track.Pieces():
            rows, cols, times, *labels = piece.AsRowsColsTimes(
                with_labels=with_cell_labels
            )

            axes.plot3D(rows, cols, times, color=color)

            if with_cell_labels:
                for row, col, time, label in zip(rows, cols, times, labels[0]):
                    axes.text(
                        row,
                        col,
                        time,
                        str(label),
                        fontsize="x-small",
                        color=color,
                    )
            if with_track_labels and (piece.label is not None):
                axes.text(
                    rows[-1],
                    cols[-1],
                    times[-1] + 0.25,
                    str(piece.label),
                    fontsize="x-small",
                    color=color,
                    bbox={
                        "facecolor": "none",
                        "edgecolor": color,
                        "boxstyle": "round",
                    },
                )

    mappable = colormap_t.ScalarMappable(cmap=colormap)
    figure.colorbar(mappable, ax=axes)

    FinalizeDisplay(figure, figure_name, show_and_wait, archiver)


def ShowUnstructuredTracking3D(
    sequence: sequence_t,
    /,
    *,
    with_cell_labels: bool = True,
    show_and_wait: bool = True,
    figure_name: str = "tracking 3D (unstructured)",
    archiver: archiver_t = None,
) -> None:
    """"""
    invalids = sequence.invalid_tracks["unstructured"]
    if invalids is None:
        return

    figure, axes = FigureAndAxes()

    colors = _MATPLOTLIB_COLORS
    for t_idx, track in enumerate(invalids):
        color_idx = t_idx % colors.__len__()

        for time_point, *cells, _ in track.segments_iterator:
            rows, cols = tuple(zip(*(_cll.centroid.tolist() for _cll in cells)))
            times = (time_point, time_point + 1)

            axes.plot3D(rows, cols, times, colors[color_idx])

            if with_cell_labels:
                labels = tuple(_cll.label for _cll in cells)
                for row, col, time, label in zip(rows, cols, times, labels[0]):
                    axes.text(
                        row,
                        col,
                        time,
                        str(label),
                        fontsize="x-small",
                        color=colors[color_idx],
                    )

    FinalizeDisplay(figure, figure_name, show_and_wait, archiver)
