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

from typing import Any, Optional, Sequence, Tuple, Union

import matplotlib.pyplot as pypl
import numpy as nmpy
import skimage.measure as msre
from matplotlib.lines import Line2D as line_t
from matplotlib.text import Annotation as annotation_t

from cell_tracking_BC.in_out.file.archiver import archiver_t
from cell_tracking_BC.type.frame import frame_t
from cell_tracking_BC.type.segmentation import compartment_t
from cell_tracking_BC.type.sequence import sequence_h, sequence_t
from cell_tracking_BC.type.tracks import tracks_t


array_t = nmpy.ndarray


ANNOTATION_SIZE = "x-small"
COLOR_DEFAULT = "red"
COLOR_HIGHLIGHT = "magenta"
BBOX_STYLE_DEFAULT = {
    "boxstyle": "round",
    "edgecolor": (1.0, 0.0, 0.0, 0.5),
    "facecolor": 4 * (0.0,),
}
BBOX_STYLE_HIGHLIGHT = {
    "boxstyle": "round",
    "edgecolor": (1.0, 0.0, 1.0, 0.5),
    "facecolor": 4 * (0.0,),
}


def AnnotateCells(
    frame: Union[array_t, frame_t],
    cell_contours: Optional[Sequence[array_t]],
    with_cell_labels: bool,
    cell_frame: Optional[frame_t],
    tracks: Optional[tracks_t],
    axes: pypl.Axes,
    /,
    *,
    highlighted: int = -1,
    elevation: float = None,
) -> Sequence[Tuple[int, annotation_t]]:
    """"""
    output = []

    if with_cell_labels or (tracks is not None):
        if elevation is None:
            to_be_removed = filter(
                lambda _art: isinstance(_art, (annotation_t, line_t)),
                axes.get_children(),
            )
            # tuple: to build a static list before iterative removal, just in case
            for annotation in tuple(to_be_removed):
                annotation.remove()

            AnnotateCell = lambda _pos, _txt, _add: axes.annotate(
                _txt,
                _pos,
                ha="center",
                fontsize=ANNOTATION_SIZE,
                fontweight="bold",
                **_add,
            )
        else:
            AnnotateCell = lambda _pos, _txt, _add: axes.text(
                *_pos, _txt, fontsize=ANNOTATION_SIZE, fontweight="bold", **_add
            )

        if cell_frame is None:
            labeled = msre.label(frame, connectivity=1)
            cells = msre.regionprops(labeled)
        else:
            cells = cell_frame.cells
        assert hasattr(cells[0], "centroid") and hasattr(
            cells[0], "label"
        ), "Please contact developer about API change"

        additionals = {"color": COLOR_DEFAULT, "bbox": BBOX_STYLE_DEFAULT}
        for cell in cells:
            if elevation is None:
                position = nmpy.flipud(cell.centroid)
            else:
                position = (*cell.centroid, elevation)
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
            if cell.label == highlighted:
                additionals["color"] = COLOR_HIGHLIGHT
            else:
                additionals["color"] = COLOR_DEFAULT
            if "\n" in text:
                if cell.label == highlighted:
                    additionals["bbox"] = BBOX_STYLE_HIGHLIGHT
                else:
                    additionals["bbox"] = BBOX_STYLE_DEFAULT
            elif "bbox" in additionals:
                del additionals["bbox"]
            annotation = AnnotateCell(position, text, additionals)
            output.append((cell.label, annotation))

    # Leave this block after cell annotation since, if placed before, the (new) contours are considered as previous
    # artists and removed.
    if cell_contours is not None:
        for contour in cell_contours:
            axes.plot(
                contour[:, 1], contour[:, 0], linestyle=":", color=(0.0, 1.0, 1.0, 0.3)
            )

    return output


def CellContours(
    sequence: sequence_h, with_segmentation: bool, /
) -> Optional[Sequence[Sequence[array_t]]]:
    """"""
    if (
        with_segmentation
        and isinstance(sequence, sequence_t)
        and (sequence.segmentations is not None)
    ):
        output = []
        for segmentation in sequence.segmentations.CompartmentsWithVersion(
            compartment_t.CELL
        ):
            output.append(msre.find_contours(segmentation))
    else:
        output = None

    return output


def CellTracks(sequence: sequence_h, with_track_labels: bool, /) -> Optional[tracks_t]:
    """"""
    with_track_labels = (
        with_track_labels
        and isinstance(sequence, sequence_t)
        and (sequence.tracks is not None)
    )
    if with_track_labels:
        output = sequence.tracks
    else:
        output = None

    return output


def ShowPreparedFigure(_: Any, should_run_event_loop: bool, /) -> None:
    """"""
    pypl.show(block=should_run_event_loop)


def FinalizeDisplay(
    figure: pypl.Figure, figure_name: str, show_and_wait: bool, archiver: archiver_t, /
) -> None:
    """"""
    if archiver is not None:
        figure.canvas.draw_idle()
        archiver.Store(figure, figure_name)

    if show_and_wait:
        pypl.show()


def FigureContents(figure: pypl.Figure, /) -> array_t:
    """
    Alternative:
        - fig.canvas.renderer._renderer?
        - Agg Buffer To Array: np.array(canvas.renderer.buffer_rgba())
    """
    height, width = figure.canvas.get_width_height()
    output = nmpy.fromstring(figure.canvas.tostring_rgb(), dtype=nmpy.uint8)
    output.shape = (width, height, 3)

    return output
