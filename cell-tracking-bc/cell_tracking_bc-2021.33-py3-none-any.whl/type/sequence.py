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

import dataclasses as dcls
import sys as sstm
from pathlib import Path as path_t
from typing import Any, Callable, Dict, Iterator, Optional, Sequence, Tuple, Union

import numpy as nmpy
import scipy.ndimage as imge
import tqdm

from cell_tracking_BC.in_out.text.uid import ShortID
from cell_tracking_BC.type.cell import cell_t
from cell_tracking_BC.type.frame import frame_t, transform_h
from cell_tracking_BC.type.segmentation import segmentation_t
from cell_tracking_BC.type.segmentations import segmentations_t
from cell_tracking_BC.type.track import (
    forking_track_t,
    single_track_t,
    unstructured_track_t,
)
from cell_tracking_BC.type.tracks import tracks_t


array_t = nmpy.ndarray
invalid_tracks_h = Dict[
    str, Sequence[Union[unstructured_track_t, single_track_t, forking_track_t]]
]
channel_computation_h = Callable[[Dict[str, array_t], Dict[str, Any]], array_t]
morphological_feature_computation_h = Callable[
    [cell_t, Dict[str, Any]], Union[Any, Sequence[Any]]
]
radiometric_feature_computation_h = Callable[
    [cell_t, Union[array_t, Sequence[array_t]], Dict[str, Any]],
    Union[Any, Sequence[Any]],
]


@dcls.dataclass(repr=False, eq=False)
class sequence_t:

    path: Optional[path_t] = None
    shape: Tuple[int, int] = None
    original_length: int = None
    length: int = None
    base_channels: Sequence[str] = None
    frames_of_channel: Dict[str, Sequence[Union[array_t, frame_t]]] = None
    cell_channel: str = None  # Name of channel whose frames store the segmented cells
    segmentations: segmentations_t = dcls.field(init=False, default=None)
    tracks: tracks_t = dcls.field(init=False, default=None)
    invalid_tracks: invalid_tracks_h = dcls.field(init=False, default=None)

    @classmethod
    def NewFromFrames(
        cls,
        frames: array_t,
        in_channel_names: Sequence[Optional[str]],
        path: path_t,
        /,
        *,
        first_frame: int = 0,
        last_frame: int = nmpy.iinfo(int).max,
    ) -> sequence_t:
        """
        in_channel_names: names equal to None or "___" or "---" indicate channels that should be discarded
        """
        # TODO: make this function accept various input shapes thanks to an additional arrangement parameter of the
        #     form THRC, T=time, H=channel, RC= row column. This requires that SequenceFromPath deals with TH combined
        #     dimension.
        if (n_dims := frames.ndim) not in (3, 4):
            raise ValueError(
                f"{n_dims}: Invalid number of dimensions of sequence with shape {frames.shape}; "
                f"Expected=3 or 4=(TIME POINTS*CHANNELS)xROWSxCOLUMNS or "
                f"TIME POINTSxCHANNELSxROWSxCOLUMNS"
            )

        n_in_channels = in_channel_names.__len__()

        frames_of_channel = {}
        for name in in_channel_names:
            if (name is not None) and (name != "___") and (name != "---"):
                frames_of_channel[name] = []
        base_channel_names = tuple(frames_of_channel.keys())

        if n_dims == 3:
            c_idx = n_in_channels - 1
            time_point = -1
            for raw_frame in frames:
                c_idx += 1
                if c_idx == n_in_channels:
                    c_idx = 0
                    time_point += 1

                if time_point < first_frame:
                    continue
                elif time_point > last_frame:
                    break

                name = in_channel_names[c_idx]
                if name in base_channel_names:
                    frame = frame_t(raw_frame)
                    frames_of_channel[name].append(frame)
        else:
            for time_point, raw_frame in enumerate(frames):
                if time_point < first_frame:
                    continue
                elif time_point > last_frame:
                    break

                for c_idx, channel in enumerate(raw_frame):
                    name = in_channel_names[c_idx]
                    if name in base_channel_names:
                        frame = frame_t(channel)
                        frames_of_channel[name].append(frame)

        frames_of_base_channel = frames_of_channel[base_channel_names[0]]
        shape = frames_of_base_channel[0].shape
        length = frames_of_base_channel.__len__()
        instance = cls(
            path=path,
            shape=shape,
            original_length=frames.__len__(),
            length=length,
            base_channels=base_channel_names,
            frames_of_channel=frames_of_channel,
        )

        return instance

    @property
    def channels(self) -> Sequence[str]:
        """
        Names of channels read from file (base channels) and computed channels
        """
        return tuple(self.frames_of_channel.keys())

    @property
    def has_cells(self) -> bool:
        """"""
        return self.cell_channel is not None

    @property
    def cell_frames(self) -> Sequence[frame_t]:
        """"""
        return self.Frames(channel=self.cell_channel)

    def Frames(
        self,
        /,
        *,
        channel: Union[str, Sequence[str]] = None,
    ) -> Union[
        Sequence[Union[array_t, frame_t]],
        Iterator[Sequence[Union[array_t, frame_t]]],
    ]:
        """
        channel: None=all (!) base channels; Otherwise, only (a) base channel name(s) can be passed
        as_iterator: Always considered True if channel is None or a sequence of channel names
        """
        if isinstance(channel, str):
            return self.frames_of_channel[channel]
        else:
            return self._FramesForMultipleChannels(channel)

    def _FramesForMultipleChannels(
        self, channels: Optional[Sequence[str]], /
    ) -> Iterator[Sequence[Union[array_t, frame_t]]]:
        """
        /!\ If "channels" contains both base and non-base channels, then the returned tuples will contain both array_t
        and frame_t elements (but frame_t is a subclass of array_t, so...).
        """
        if channels is None:
            channels = self.base_channels

        for f_idx in range(self.length):
            frames = (self.frames_of_channel[_chl][f_idx] for _chl in channels)

            yield tuple(frames)

    @property
    def cells_iterator(self) -> Iterator[Sequence[cell_t]]:
        """"""
        for frame in self.cell_frames:
            yield frame.cells

    def ApplyTransform(
        self,
        Transform: transform_h,
        /,
        *,
        channel: Union[str, Sequence[str]] = None,
        **kwargs,
    ) -> None:
        """
        channel: None=all (!)
        """
        if channel is None:
            channels = self.base_channels
        elif isinstance(channel, str):
            channels = (channel,)
        else:
            channels = channel

        for channel in channels:
            targets = self.Frames(channel=channel)
            references_sets = self.Frames(channel=self.channels)
            for target, references in zip(targets, references_sets):
                refs_as_dict = {
                    _nme: _frm for _nme, _frm in zip(self.channels, references)
                }
                target.ApplyTransform(Transform, channels=refs_as_dict, **kwargs)

    def AddComputedChannel(
        self, name: str, ChannelComputation: channel_computation_h, /, **kwargs
    ) -> None:
        """"""
        computed = []
        for frames in self.Frames(channel=self.channels):
            frames_as_dict = {_nme: _frm for _nme, _frm in zip(self.channels, frames)}
            computed.append(ChannelComputation(frames_as_dict, **kwargs))

        self.frames_of_channel[name] = computed

    def AddCellsFromSegmentations(
        self,
        channel: str,
        segmentations: segmentations_t,
    ) -> None:
        """
        Segmentation are supposed to be binary (as opposed to already labeled)
        """
        self.cell_channel = channel
        self.segmentations = segmentations

        for frame, segmentation in zip(self.cell_frames, segmentations):
            frame.AddCellsFromSegmentation(segmentation)

    def AddTracks(
        self,
        tracks: tracks_t,
        invalid_tracks: Optional[Sequence[unstructured_track_t]],
        /,
        max_root_time_point: int = 0,
        min_length: int = 1,
        min_min_length: int = 1,
        max_n_children: int = 2,
    ) -> None:
        """"""
        valid_tracks = tracks
        all_invalid_tracks = {
            "unstructured": invalid_tracks,
            "single": [],
            "forking": [],
        }
        additional_forking = {
            "min_min_length": min_min_length,
            "max_n_children": max_n_children,
        }

        t_idx = 0
        while t_idx < valid_tracks.__len__():
            track = valid_tracks[t_idx]
            if isinstance(track, single_track_t):
                arguments = {}
                where = "single"
            else:
                arguments = additional_forking
                where = "forking"
            issues = track.Issues(max_root_time_point, min_length, **arguments)
            if issues is None:
                t_idx += 1
            else:
                del valid_tracks[t_idx]
                track.issues = issues
                all_invalid_tracks[where].append(track)

        for key, value in all_invalid_tracks.items():
            if (value is not None) and (value.__len__() == 0):
                all_invalid_tracks[key] = None
        if all(_elm is None for _elm in all_invalid_tracks.values()):
            all_invalid_tracks = None

        self.tracks = valid_tracks
        self.invalid_tracks = all_invalid_tracks

    def PrintValidInvalidSummary(self) -> None:
        """"""
        n_invalids = []
        invalid_issues = {}
        for key, tracks in self.invalid_tracks.items():
            if tracks is None:
                number = f"{key}: None"
            else:
                number = f"{key}: {tracks.__len__()}"

                if isinstance(tracks[0], unstructured_track_t):
                    Issues = lambda _tck: _tck.graph["issues"]
                else:
                    Issues = lambda _tck: _tck.issues
                issues = tuple("; ".join(Issues(_tck)) for _tck in tracks)
                invalid_issues[key] = "\n".join(issues)

            n_invalids.append(number)

        n_invalids = ", ".join(n_invalids)
        invalid_issues = "\n".join(
            f"{_key}:\n{_val}" for _key, _val in invalid_issues.items()
        )
        print(
            f"Tracks: valid={self.tracks.__len__()}, invalid={n_invalids}\n{invalid_issues}"
        )

    def AddMorphologicalFeature(
        self,
        name: Union[str, Sequence[str]],
        Feature: morphological_feature_computation_h,
        /,
        **kwargs,
    ) -> None:
        """
        name: If an str, then the value returned by Feature will be considered as a whole, whether it is actually a
        single value or a value container. If a sequence of str's, then the object returned by Feature will be iterated
        over as many times as the length of this sequence.
        """
        # Otherwise tqdm might print before previous prints have been flushed
        sstm.stdout.flush()

        cells_iterator = tqdm.tqdm(
            self.cells_iterator,
            total=self.length,
            desc=f'Feature Computation "{name}"',
        )
        if isinstance(name, str):
            for cells in cells_iterator:
                for cell in cells:
                    feature = Feature(cell, **kwargs)
                    cell.AddFeature(name, feature)
        else:
            names = name
            for cells in cells_iterator:
                for cell in cells:
                    features = Feature(cell, **kwargs)
                    for name, feature in zip(names, features):
                        cell.AddFeature(name, feature)

    def AddRadiometricFeature(
        self,
        name: Union[str, Sequence[str]],
        Feature: radiometric_feature_computation_h,
        channel: Union[str, Sequence[str]],
        /,
        **kwargs,
    ) -> None:
        """
        See AddMorphologicalFeature
        """
        # Otherwise tqdm might print before previous prints have been flushed
        sstm.stdout.flush()

        frame_iterator = tqdm.tqdm(
            zip(self.cell_frames, self.Frames(channel=channel)),
            total=self.length,
            desc=f'Feature Computation "{name}"',
        )
        for frame_w_cells, frame in frame_iterator:
            for cell in frame_w_cells.cells:
                if isinstance(name, str):
                    feature = Feature(cell, frame, **kwargs)
                    cell.AddFeature(name, feature)
                else:
                    features = Feature(cell, frame, **kwargs)
                    for f_name, feature in zip(name, features):
                        cell.AddFeature(f_name, feature)

    @property
    def available_cell_features(self) -> Sequence[str]:
        """"""
        one_cell = self.cell_frames[0].cells[0]

        return one_cell.available_features

    @staticmethod
    def FeatureEvolutionAlongTrack(
        track: single_track_t, feature: str, /
    ) -> Sequence[Any]:
        """"""
        if feature in track[0].features:
            return tuple(_cll.features[feature] for _cll in track)

        return (track.length + 1) * [None]

    def FeatureEvolutionsAlongAllTracks(
        self, feature: str, /
    ) -> Dict[int, Tuple[single_track_t, Sequence[Any]]]:
        """"""
        output = {}

        for track in self.tracks.single_tracks_iterator:
            output[track.label] = (
                track,
                sequence_t.FeatureEvolutionAlongTrack(track, feature),
            )

        return output

    def ClearContents(self):
        """
        To free up some memory when all processing has been done
        """
        for frames in self.Frames():
            for frame in frames:
                frame.ClearContents()

    def __str__(self) -> str:
        """"""
        if self.invalid_tracks is None:
            invalid_tracks = "None"
        else:
            invalid_tracks = (
                f'{self.invalid_tracks["unstructured"]=}\n'
                f'    {self.invalid_tracks["single"]=}\n'
                f'    {self.invalid_tracks["forking"]=}'
            )
        return (
            f"{self.__class__.__name__.upper()}.{ShortID(id(self))}:\n"
            f"    {self.path=}\n"
            f"    {self.base_channels=}\n"
            f"    {self.channels=}\n"
            f"    {self.shape=}\n"
            f"    {self.original_length=}\n"
            f"    {self.length=}\n"
            f"    {self.tracks=}\n"
            f"    {invalid_tracks=}\n"
        )


sequence_h = Union[
    Sequence[array_t], Sequence[segmentation_t], segmentations_t, sequence_t
]


def BoundingBoxSlices(sequence: array_t, /) -> Sequence[slice]:
    """
    sequence: as an XYT-volume
    """
    min_reduction = nmpy.amin(sequence, axis=-1)
    max_reduction = nmpy.amax(sequence, axis=-1)
    constant = nmpy.any(min_reduction != max_reduction, axis=-1)
    output = imge.find_objects(constant)[0]

    return output
