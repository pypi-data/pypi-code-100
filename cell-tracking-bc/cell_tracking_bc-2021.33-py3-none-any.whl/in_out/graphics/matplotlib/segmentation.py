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

from typing import Optional, Union

import matplotlib.pyplot as pypl

import cell_tracking_BC.in_out.graphics.matplotlib.generic as gphc
import cell_tracking_BC.in_out.graphics.matplotlib.generic_3d as gph3
from cell_tracking_BC.in_out.file.archiver import archiver_t
from cell_tracking_BC.in_out.graphics.matplotlib.generic_2d import sequence_2D_t
from cell_tracking_BC.type.segmentation import compartment_t
from cell_tracking_BC.type.segmentations import segmentations_t
from cell_tracking_BC.type.sequence import sequence_h, sequence_t


def ShowSegmentation(
    sequence: sequence_h,
    /,
    *,
    compartment: compartment_t = compartment_t.CELL,
    version: str = None,
    with_cell_labels: bool = True,
    with_track_labels: bool = True,
    mode: str = "2d+t",
    keep_every: int = 2,
    show_and_wait: bool = True,
    with_ticks: bool = True,
    figure_name: str = "segmentation",
    archiver: archiver_t = None,
) -> Optional[Union[pypl.Figure, sequence_2D_t]]:
    """
    mode: see ShowSequence
    """
    output = None

    if mode == "2d+t":
        viewer = sequence_2D_t.NewForSegmentation(
            sequence,
            version=version,
            with_cell_labels=with_cell_labels,
            with_track_labels=with_track_labels,
            with_ticks=with_ticks,
            figure_name=figure_name,
            archiver=archiver,
        )
        if show_and_wait:
            pypl.show()
        else:
            output = viewer
    elif mode in ("mille-feuille", "tunnels"):
        if isinstance(sequence, (segmentations_t, sequence_t)):
            if isinstance(sequence, segmentations_t):
                segmentations = sequence
            else:
                segmentations = sequence.segmentations
            segmentations = segmentations.CompartmentsWithVersion(compartment)
        else:
            segmentations = sequence

        figure, axes = gph3.FigureAndAxes()
        if mode == "mille-feuille":
            if isinstance(sequence, sequence_t) and sequence.has_cells:
                cell_frames = sequence.cell_frames
            else:
                cell_frames = None
            tracks = gphc.CellTracks(sequence, with_track_labels)
            gph3.ShowFramesAsMilleFeuille(
                segmentations,
                None,
                with_cell_labels,
                cell_frames,
                tracks,
                axes,
                keep_every=keep_every,
            )
        else:
            gph3.ShowFramesAsTunnels(segmentations, axes, keep_every=keep_every)

        if not show_and_wait:
            output = figure
        gphc.FinalizeDisplay(figure, figure_name, show_and_wait, archiver)
    else:
        raise ValueError(
            f'{mode}: Invalid mode; Expected="2d+t", "mille-feuille", "tunnels"'
        )

    return output
