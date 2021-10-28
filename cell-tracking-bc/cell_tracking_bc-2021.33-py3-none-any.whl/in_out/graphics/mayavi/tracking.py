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

from mayavi import mlab

from cell_tracking_BC.in_out.file.archiver import archiver_t
from cell_tracking_BC.type.sequence import sequence_t


def ShowTracking(
    sequence: sequence_t,
    /,
    *,
    with_track_labels: bool = True,
    with_cell_labels: bool = True,
    show_and_wait: bool = True,
    figure_name: str = "tracking",
    _: archiver_t = None,
) -> None:
    """"""
    figure = mlab.figure(figure=figure_name, bgcolor=(1, 1, 1))
    mlab.axes(
        xlabel="row positions",
        ylabel="column positions",
        zlabel="time points",
        figure=figure,
    )
    mlab.outline(figure=figure)

    size = 0.5 * sum(sequence.shape)
    time_scale = size / sequence.length

    colors = (
        (0, 0, 1),
        (0, 1, 0),
        (1, 0, 0),
        (0, 1, 1),
        (1, 0, 1),
        (1, 1, 0),
        (0, 0, 0),
    )
    for t_idx, track in enumerate(sequence.tracks):
        color_idx = t_idx % colors.__len__()

        for piece in track.Pieces():
            rows, cols, times, *labels = piece.AsRowsColsTimes(
                with_labels=with_cell_labels
            )
            times = tuple(time_scale * _tme for _tme in times)

            # tube_radius=0.025*size
            mlab.plot3d(rows, cols, times, color=colors[color_idx], figure=figure)

            if with_cell_labels:
                for row, col, time, label in zip(rows, cols, times, labels[0]):
                    mlab.text3d(
                        row,
                        col,
                        time,
                        str(label),
                        color=colors[color_idx],
                        figure=figure,
                    )
            if with_track_labels and (piece.label is not None):
                mlab.text3d(
                    rows[-1],
                    cols[-1],
                    times[-1] + 0.25,
                    str(piece.label),
                    color=colors[color_idx],
                    figure=figure,
                )

    if show_and_wait:
        mlab.show()
