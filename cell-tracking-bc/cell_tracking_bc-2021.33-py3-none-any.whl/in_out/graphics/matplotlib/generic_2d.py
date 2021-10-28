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
import datetime as dttm
import re as regx
from pathlib import Path as path_t
from typing import Callable, Dict, Optional, Sequence, Tuple, Union

import matplotlib.pyplot as pypl
import numpy as nmpy
import tifffile as tiff
from matplotlib import rc as SetMatplotlibConfig
from matplotlib.backend_bases import KeyEvent as key_event_t
from matplotlib.backend_bases import MouseEvent as mouse_event_t
from matplotlib.image import AxesImage as axes_image_t
from matplotlib.text import Annotation as annotation_t
from matplotlib.widgets import Slider as slider_t

import cell_tracking_BC.in_out.graphics.matplotlib.generic as gphc
from cell_tracking_BC.in_out.file.archiver import archiver_t
from cell_tracking_BC.in_out.graphics.matplotlib.generic import (
    BBOX_STYLE_DEFAULT,
    BBOX_STYLE_HIGHLIGHT,
    COLOR_DEFAULT,
    COLOR_HIGHLIGHT,
)
from cell_tracking_BC.type.frame import frame_t
from cell_tracking_BC.type.segmentation import compartment_t, segmentation_t
from cell_tracking_BC.type.segmentations import segmentations_t
from cell_tracking_BC.type.sequence import sequence_h, sequence_t, BoundingBoxSlices
from cell_tracking_BC.type.tracks import tracks_t


array_t = nmpy.ndarray
axes_2d_t = pypl.Axes

all_versions_h = Dict[
    str, Tuple[Tuple[int, int], Union[Sequence[array_t], Sequence[frame_t]]]
]


@dtcl.dataclass(repr=False, eq=False)
class sequence_2D_t:

    figure: pypl.Figure
    axes: axes_2d_t
    frame: axes_image_t
    slider: Optional[slider_t]

    all_versions: all_versions_h
    current_version: str = None
    current_time_point: int = -1  # Used only when slider is None
    current_label: int = -1

    cell_contours: Sequence[
        Sequence[array_t]
    ] = None  # Only meaningful for NewForChannels
    with_cell_labels: bool = (
        False  # Using frame labeling for array_t's, or cell_frames below for sequence_t
    )
    cell_frames: Sequence[frame_t] = None
    tracks: tracks_t = None
    annotations: Sequence[Tuple[int, annotation_t]] = None

    @classmethod
    def NewForChannels(
        cls,
        sequence: Union[Sequence[array_t], sequence_t],
        /,
        *,
        channel: str = None,
        with_segmentation: bool = False,
        with_cell_labels: bool = False,
        with_track_labels: bool = False,
        in_axes: axes_2d_t = None,
        with_ticks: bool = True,
        with_colorbar: bool = True,
        figure_name: str = "sequence",
        archiver: archiver_t = None,
    ) -> sequence_2D_t:
        """"""
        with_cell_labels = (
            with_cell_labels and isinstance(sequence, sequence_t) and sequence.has_cells
        )
        if with_cell_labels:
            cell_frames = sequence.cell_frames
        else:
            cell_frames = None

        instance = cls._NewForSequence(
            sequence,
            _AllChannelsOfSequence,
            version=channel,
            with_segmentation=with_segmentation,
            with_cell_labels=with_cell_labels,
            cell_frames=cell_frames,
            with_track_labels=with_track_labels,
            in_axes=in_axes,
            with_ticks=with_ticks,
            figure_name=figure_name,
            archiver=archiver,
        )
        if with_colorbar:
            instance.figure.colorbar(instance.frame, ax=instance.axes)

        return instance

    @classmethod
    def NewForSegmentation(
        cls,
        sequence: sequence_h,
        /,
        *,
        version: str = None,
        with_cell_labels: bool = True,
        with_track_labels: bool = True,
        in_axes: axes_2d_t = None,
        with_ticks: bool = True,
        figure_name: str = "segmentation",
        archiver: archiver_t = None,
    ) -> sequence_2D_t:
        """"""
        if (
            isinstance(sequence, Sequence)
            and isinstance(sequence[0], segmentation_t)
            and not isinstance(sequence, segmentations_t)
        ):
            new_sequence = segmentations_t()
            for segmentation in sequence:
                new_sequence.append(segmentation)
            sequence = new_sequence

        if with_cell_labels and isinstance(sequence, sequence_t) and sequence.has_cells:
            cell_frames = sequence.cell_frames
        else:
            cell_frames = None

        return cls._NewForSequence(
            sequence,
            _AllSegmentationsOfSequence,
            version=version,
            with_cell_labels=with_cell_labels,
            cell_frames=cell_frames,
            with_track_labels=with_track_labels,
            in_axes=in_axes,
            with_ticks=with_ticks,
            figure_name=figure_name,
            archiver=archiver,
        )

    @classmethod
    def NewForAllStreams(
        cls,
        sequence: sequence_t,
        /,
        *,
        version: str = None,
        with_segmentation: bool = False,
        with_cell_labels: bool = False,
        with_track_labels: bool = False,
        in_axes: axes_2d_t = None,
        with_ticks: bool = True,
        with_colorbar: bool = True,
        figure_name: str = "sequence",
        archiver: archiver_t = None,
    ) -> sequence_2D_t:
        """"""
        with_cell_labels = with_cell_labels and sequence.has_cells
        if with_cell_labels:
            cell_frames = sequence.cell_frames
        else:
            cell_frames = None

        instance = cls._NewForSequence(
            sequence,
            _AllStreamsOfSequence,
            version=version,
            with_segmentation=with_segmentation,
            with_cell_labels=with_cell_labels,
            cell_frames=cell_frames,
            with_track_labels=with_track_labels,
            in_axes=in_axes,
            with_ticks=with_ticks,
            figure_name=figure_name,
            archiver=archiver,
        )
        if with_colorbar:
            instance.figure.colorbar(instance.frame, ax=instance.axes)

        return instance

    @classmethod
    def _NewForSequence(
        cls,
        sequence: sequence_h,
        AllVersionsOfSequence: Callable[[sequence_h], Tuple[all_versions_h, str]],
        /,
        *,
        version: str = None,
        with_segmentation: bool = False,
        with_cell_labels: bool = True,
        cell_frames: Sequence[frame_t] = None,
        with_track_labels: bool = True,
        in_axes: axes_2d_t = None,
        with_ticks: bool = True,
        figure_name: str = "sequence",
        archiver: archiver_t = None,
    ) -> sequence_2D_t:
        """"""
        if in_axes is None:
            figure = pypl.figure()
            axes = figure.subplots()
        else:
            figure = in_axes.figure
            axes = in_axes
        if not with_ticks:
            axes.set_axis_off()

        all_versions, current_version = AllVersionsOfSequence(sequence)
        if version is not None:
            current_version = version
        if (more_than_one := (all_versions.__len__() > 1)) and axes.axison:
            axes.set_title(current_version)

        cell_contours = gphc.CellContours(sequence, with_segmentation)
        tracks = gphc.CellTracks(sequence, with_track_labels)

        frame, n_frames, cell_annotations = _ShowFirstFrame(
            all_versions,
            current_version,
            cell_contours,
            with_cell_labels,
            cell_frames,
            tracks,
            axes,
        )

        if in_axes is None:
            slider_axes = figure.add_axes([0.15, 0.04, 0.7, 0.03])
            slider = slider_t(
                slider_axes,
                "Time Point",
                0,
                n_frames - 1,
                valinit=0,
                valstep=1,
            )
            current_time_point = None
        else:
            slider = None
            current_time_point = 0

        instance = cls(
            figure=figure,
            axes=axes,
            frame=frame,
            slider=slider,
            all_versions=all_versions,
            current_version=current_version,
            current_time_point=current_time_point,
            cell_contours=cell_contours,
            with_cell_labels=with_cell_labels,
            tracks=tracks,
            cell_frames=cell_frames,
            annotations=cell_annotations,
        )

        SetMatplotlibConfig("keymap", save=[])
        figure.canvas.mpl_connect("key_press_event", instance._OnKeyPress)
        if more_than_one:
            figure.canvas.mpl_connect("button_press_event", instance._OnButtonPress)
        if slider is not None:
            figure.canvas.mpl_connect("scroll_event", instance._OnScrollEvent)

        if in_axes is None:
            gphc.FinalizeDisplay(figure, figure_name, False, archiver)

        return instance

    def _OnKeyPress(
        self,
        event: key_event_t,
        /,
    ) -> None:
        """"""
        if event.key.lower() == "s":
            print("Sequence saving in progress...")
            volume = self.AsAnnotatedVolume()

            illegal = "[^-_a-zA-Z0-9]"
            version = regx.sub(illegal, "", self.current_version)
            now = regx.sub(illegal, "-", dttm.datetime.now().isoformat())
            path = path_t.home() / f"sequence-{version}-{now}.tif"
            if path.exists():
                print(f"{path}: Existing path; Cannot override")
                return

            tiff.imwrite(
                str(path),
                volume,
                photometric="rgb",
                compression="deflate",
                planarconfig="separate",
                metadata={"axes": "XYZCT"},
            )
            print(f"Annotated sequence saved at: {path}")

    def _OnButtonPress(
        self,
        event: mouse_event_t,
        /,
    ) -> None:
        """"""
        if event.inaxes is self.axes:
            self.ShowNextVersion()

    def _OnScrollEvent(self, event: mouse_event_t) -> None:
        """"""
        value = self.slider.val
        new_value = round(value + nmpy.sign(event.step))
        new_value = min(max(new_value, self.slider.valmin), self.slider.valmax)
        if new_value != value:
            self.ShowFrame(time_point=new_value)

    def ShowFrame(
        self,
        /,
        *,
        version: str = None,
        time_point: Union[int, float] = None,
        highlighted: int = -1,
        should_update_limits: bool = False,
        should_draw: bool = True,
    ) -> None:
        """"""
        if version is None:
            version = self.current_version
        if self.slider is None:
            current_time_point = self.current_time_point
        else:
            current_time_point = self.slider.val
        if time_point is None:
            time_point = current_time_point
        else:
            time_point = int(time_point)

        version_is_new = version != self.current_version
        time_point_is_new = time_point != current_time_point

        if version_is_new or time_point_is_new:
            interval, frames = self.all_versions[version]
            frame = frames[time_point]
            self.frame.set_array(frame)
            if should_update_limits:
                self.frame.set_clim(*interval)
        else:
            frame = None

        if self.annotations is not None:
            if time_point_is_new:
                if self.cell_contours is None:
                    contours = None
                else:
                    contours = self.cell_contours[time_point]
                if self.cell_frames is None:
                    cell_frame = None
                else:
                    cell_frame = self.cell_frames[time_point]

                self.annotations = gphc.AnnotateCells(
                    frame,
                    contours,
                    self.with_cell_labels,
                    cell_frame,
                    self.tracks,
                    self.axes,
                    highlighted=highlighted,
                )
                self.current_label = highlighted
            elif highlighted > 0:
                self.HighlightAnnotation(highlighted, should_draw=False)

        if version_is_new:
            if self.axes.axison:
                self.axes.set_title(version)
            self.current_version = version

        if time_point_is_new:
            if self.slider is None:
                self.current_time_point = time_point
            else:
                self.slider.set_val(time_point)

        if should_draw:
            self.figure.canvas.draw_idle()

    def ShowNextVersion(self, /, *, should_draw: bool = True) -> None:
        """"""
        all_names = tuple(self.all_versions.keys())
        where = all_names.index(self.current_version)
        where = (where + 1) % all_names.__len__()
        new_version = all_names[where]

        self.ShowFrame(
            version=new_version, should_update_limits=True, should_draw=should_draw
        )

    def HighlightAnnotation(self, label: int, /, *, should_draw: bool = True) -> None:
        """
        If label is <= 0 or > max cell label in current frame, then un-highlights all annotations
        """
        if label == self.current_label:
            return

        for annotation in self.annotations:
            text = annotation[1]
            if label == annotation[0]:
                text.set_color(COLOR_HIGHLIGHT)
                if "\n" in text.get_text():
                    text.set_bbox(BBOX_STYLE_HIGHLIGHT)
            else:
                text.set_color(COLOR_DEFAULT)
                if "\n" in text.get_text():
                    text.set_bbox(BBOX_STYLE_DEFAULT)

        self.current_label = label

        if should_draw:
            self.figure.canvas.draw_idle()

    def ShowAndWait(self) -> None:
        """"""
        pypl.show()

    def AsAnnotatedVolume(self) -> array_t:
        """
        See: cell_tracking_BC.in_out.file.sequence.SaveAnnotatedSequence
        """
        output = (
            None  # Cannot be initialized since content (not frame) shape is unknown
        )

        current_version = self.all_versions[self.current_version][1]
        sequence_length = current_version.__len__()

        figure, axes = FigureAndAxes()
        invisible = self.__class__._NewForSequence(
            current_version,
            _AllChannelsOfSequence,
            with_cell_labels=self.with_cell_labels,
            cell_frames=self.cell_frames,
            with_track_labels=False,
            with_ticks=False,
            in_axes=axes,
        )
        invisible.cell_contours = self.cell_contours
        invisible.tracks = self.tracks

        for time_point in range(sequence_length):
            invisible.ShowFrame(time_point=time_point, should_draw=False)
            figure.canvas.draw()  # draw_idle is not appropriate here
            content = gphc.FigureContents(figure)
            if output is None:
                output = nmpy.empty((*content.shape, sequence_length), dtype=nmpy.uint8)
            output[..., time_point] = content

        pypl.close(fig=figure)  # To prevent remaining caught in event loop

        row_slice, col_slice = BoundingBoxSlices(output)
        output = output[row_slice, col_slice, :, :]
        output = nmpy.moveaxis(output, (0, 1, 2, 3), (2, 3, 1, 0))
        output = output[:, nmpy.newaxis, :, :, :]

        return output


def _AllChannelsOfSequence(
    sequence: Union[Sequence[array_t], sequence_t]
) -> Tuple[all_versions_h, str]:
    """"""
    if isinstance(sequence, sequence_t):
        all_channels = {}
        for channel in sequence.channels:
            frames = sequence.Frames(channel=channel)
            min_value = min(nmpy.amin(_frm) for _frm in frames)
            max_value = max(nmpy.amax(_frm) for _frm in frames)
            all_channels[channel] = ((min_value, max_value), frames)
        current_channel = sequence.channels[0]
    else:
        current_channel = "MAIN"
        min_value = min(nmpy.amin(_frm) for _frm in sequence)
        max_value = max(nmpy.amax(_frm) for _frm in sequence)
        all_channels = {current_channel: ((min_value, max_value), sequence)}

    return all_channels, current_channel


def _AllSegmentationsOfSequence(sequence: sequence_h) -> Tuple[all_versions_h, str]:
    """"""
    if isinstance(sequence, (segmentations_t, sequence_t)):
        if isinstance(sequence, segmentations_t):
            segmentations = sequence
        else:
            segmentations = sequence.segmentations

        all_versions = {}
        compartments, versions = segmentations.available_versions
        for compartment in compartments:
            for version in versions:
                key = f"{compartment.name}:{version[0]}:{version[1]}"
                frames = segmentations.CompartmentsWithVersion(
                    compartment, index=version[0], name=version[1]
                )
                all_versions[key] = ((0, 1), frames)
        current_version = f"{compartment_t.CELL.name}:{versions[0][0]}:{versions[0][1]}"
    else:
        current_version = "MAIN"
        all_versions = {current_version: ((0, 1), sequence)}

    return all_versions, current_version


def _AllStreamsOfSequence(sequence: sequence_t) -> Tuple[all_versions_h, str]:
    """"""
    all_streams, current_stream = _AllChannelsOfSequence(sequence)
    all_versions, _ = _AllSegmentationsOfSequence(sequence)

    all_streams.update(all_versions)

    return all_streams, current_stream


def _ShowFirstFrame(
    all_versions: all_versions_h,
    current_version: str,
    cell_contours: Optional[Sequence[Sequence[array_t]]],
    with_cell_labels: bool,
    cell_frames: Optional[Sequence[frame_t]],
    tracks: Optional[tracks_t],
    axes: axes_2d_t,
    /,
) -> Tuple[axes_image_t, int, Optional[Sequence[Tuple[int, annotation_t]]]]:
    """"""
    interval, version = all_versions[current_version]
    first_frame = version[0]

    frame = axes.matshow(first_frame, cmap="gray")
    frame.set_clim(*interval)

    if (cell_contours is not None) or with_cell_labels or (tracks is not None):
        if cell_contours is None:
            contours = None
        else:
            contours = cell_contours[0]
        if cell_frames is None:
            cell_frame = None
        else:
            cell_frame = cell_frames[0]
        cell_annotations = gphc.AnnotateCells(
            first_frame, contours, with_cell_labels, cell_frame, tracks, axes
        )
    else:
        cell_annotations = None

    # Once the first frame has been plot, disable axes autoscale to try to speed future plots up
    axes.autoscale(enable=False)

    return frame, version.__len__(), cell_annotations


def FigureAndAxes() -> Tuple[pypl.Figure, axes_2d_t]:
    """"""
    return pypl.subplots()


def SetTimeAxisProperties(highest_value: int, axes: axes_2d_t, /) -> None:
    """"""
    axes.set_xlim(0, highest_value)
    axes.set_xticks(range(highest_value + 1))
    axes.set_xticklabels(str(_idx) for _idx in range(highest_value + 1))
