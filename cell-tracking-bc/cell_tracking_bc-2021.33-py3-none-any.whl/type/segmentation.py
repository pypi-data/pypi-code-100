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
from enum import Enum as enum_t
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union

import numpy as nmpy
import scipy.ndimage.morphology as scph
import scipy.optimize as spop
import skimage.morphology as mrph
import skimage.segmentation as sgmt
from scipy import ndimage as image_t
from scipy.spatial import distance as dstc

from cell_tracking_BC.task.jaccard import PseudoJaccard


array_t = nmpy.ndarray


class compartment_t(enum_t):
    CELL = 0
    CYTOPLASM = 1
    NUCLEUS = 2


_CELL_IDX = compartment_t.CELL.value
_CYTO_IDX = compartment_t.CYTOPLASM.value


version_id_h = Tuple[int, str]
versioned_compartment_h = Union[array_t, None, version_id_h]
version_h = Tuple[versioned_compartment_h, versioned_compartment_h]
versions_h = Dict[version_id_h, version_h]


@dtcl.dataclass(repr=False, eq=False)
class segmentation_t:

    cell: array_t = None  # dtype=bool; Never None after instantiation
    cytoplasm: array_t = None  # dtype=bool
    # nucleus = cell - cytoplasm
    version_idx: int = 0
    version_name: str = "original"
    versions: versions_h = dtcl.field(init=False, default_factory=dict)

    # TODO: check that cytoplasm as at least one hole (and at most 2 holes?)

    def __post_init__(self) -> None:
        """"""
        version = self._NewVersionFromCompartments(self.cell, self.cytoplasm)
        self.versions[self.version] = version

    @classmethod
    def NewFromCompartments(
        cls,
        /,
        *,
        cell: array_t = None,
        cytoplasm: array_t = None,
        nucleus: array_t = None,
    ) -> segmentation_t:
        """
        Valid options:
            - cell               => cytoplasm = None, nucleus = None
            - cell, cytoplasm    => nucleus = cell - cytoplasm
            - cell, nucleus      => cytoplasm = cell - nucleus
            - cytoplasm          => cell = filled cytoplasm, nucleus = cell - cytoplasm
            - cytoplasm, nucleus => cell = cytoplasm + nucleus
        """
        if cell is not None:
            cell = cell > 0
        if cytoplasm is not None:
            cytoplasm = cytoplasm > 0
        if nucleus is not None:
            nucleus = nucleus > 0
        filled_cytoplasm = None

        if (cell is None) and (cytoplasm is None):
            raise ValueError("Cytoplasm and cell arrays both None")
        if not ((cell is None) or (cytoplasm is None) or (nucleus is None)):
            raise ValueError("Nucleus, cytoplasm and cell arrays all not None")
        if not ((cell is None) or (cytoplasm is None)):
            filled_cytoplasm = scph.binary_fill_holes(cytoplasm)
            if not nmpy.array_equal(filled_cytoplasm, cell):
                raise ValueError("Cytoplasm outer borders do not coincide with cells")
        if not ((cell is None) or (nucleus is None)):
            if nmpy.any(cell[nucleus] == False):
                raise ValueError("Nuclei outer borders not restricted to cells")
        if not ((cytoplasm is None) or (nucleus is None)):
            if nmpy.any(cytoplasm[nucleus]):
                raise ValueError("Cytoplasm and nucleus arrays intersect")
            # Necessarily not already computed above since all 3 segmentations cannot be passed
            filled_cytoplasm = scph.binary_fill_holes(cytoplasm)
            union = nmpy.logical_or(cytoplasm, nucleus)
            if not nmpy.array_equal(filled_cytoplasm, union):
                raise ValueError("Cytoplasm inner borders do not coincide with nuclei")

        if cell is None:  # Then cytoplasm is not None
            if filled_cytoplasm is None:
                if nucleus is None:
                    cell = scph.binary_fill_holes(cytoplasm)
                else:
                    cell = cytoplasm.copy()
                    cell[nucleus] = True
            else:
                cell = filled_cytoplasm
        # From then on, cell is not None
        if (cytoplasm is None) and (nucleus is not None):
            cytoplasm = cell.copy()
            cytoplasm[nucleus] = False

        return cls(cell=cell, cytoplasm=cytoplasm)

    @classmethod
    def NewFromDict(cls, dictionary: Dict[str, Any], /) -> segmentation_t:
        """"""
        instance = cls()

        instance.cell = nmpy.array(dictionary["cell"])
        instance.cytoplasm = (
            nmpy.array(dictionary["cytoplasm"])
            if dictionary["cytoplasm"] is not None
            else None
        )
        instance.version_idx = dictionary["version_idx"]
        instance.version_name = dictionary["version_name"]
        instance.versions = {}

        versions = instance.versions
        for version, values in dictionary["versions"].items():
            new_values = []
            for v_idx, value in enumerate(values):
                if (value is None) or IsVersion(value):
                    new_value = value
                else:
                    new_value = nmpy.array(value)
                new_values.append(new_value)
            versions[version] = tuple(new_values)

        return instance

    @property
    def nucleus(self) -> array_t:
        """"""
        if self.cytoplasm is None:
            raise RuntimeError(
                "Requesting nucleus map in a segmentation w/o cytoplasm map"
            )

        return nmpy.logical_xor(self.cell, self.cytoplasm)

    @property
    def version(self) -> version_id_h:
        """"""
        return self.version_idx, self.version_name

    def NonNoneAsList(self) -> Tuple[List[array_t], Sequence[str]]:
        """
        For preparing calls to cell_tracking_BC.type.cell_t.NewFromMaps
        """
        if self.cytoplasm is None:
            segmentations = [self.cell]
            parameters = ("cell_map",)
        else:
            segmentations = [self.cytoplasm, self.cell]
            parameters = ("cytoplasm_map", "cell_map")

        return segmentations, parameters

    @property
    def available_versions(
        self,
    ) -> Tuple[Tuple[compartment_t, ...], Sequence[version_id_h]]:
        """
        The sequences contain tuples (version index, version basename, version name), where version name is a
        combination of version index and basename.
        """
        if self.cytoplasm is None:
            compartments = (compartment_t.CELL,)
        else:
            compartments = (
                compartment_t.CELL,
                compartment_t.CYTOPLASM,
                compartment_t.NUCLEUS,
            )

        versions = []
        for version in self.versions.keys():
            versions.append(version)

        return compartments, versions

    def LatestCompartment(self, compartment: compartment_t, /) -> array_t:
        """"""
        if compartment is compartment_t.CELL:
            return self.cell

        if compartment is compartment_t.CYTOPLASM:
            if self.cytoplasm is not None:
                return self.cytoplasm
        elif compartment is compartment_t.NUCLEUS:
            return self.nucleus

        raise ValueError(f"{compartment}: Invalid compartment, or compartment is None")

    def CompartmentWithVersion(
        self, compartment: compartment_t, /, *, index: int = None, name: str = None
    ) -> array_t:
        """
        index: if None and name is None also, then returns latest version
        """
        if (
            ((index is None) and (name is None))
            or (index == self.version_idx)
            or (name == self.version_name)
        ):
            return self.LatestCompartment(compartment)

        if index is None:
            VersionIsAMatch = lambda _ver: name == _ver[1]
        elif name is None:
            VersionIsAMatch = lambda _ver: index == _ver[0]
        else:
            VersionIsAMatch = lambda _ver: (index, name) == _ver
        for version in self.versions.keys():
            if VersionIsAMatch(version):
                output = self._ResolvedCompartmentWithVersion(compartment, version)
                if output is None:
                    break
                else:
                    return output

        raise ValueError(
            f"{compartment}/{index}/{name}: Invalid compartment/index/name combination"
        )

    def _ResolvedCompartmentWithVersion(
        self, compartment: compartment_t, version: version_id_h, /
    ) -> Optional[array_t]:
        """"""
        if compartment is compartment_t.NUCLEUS:
            if self.cytoplasm is None:
                output = None
            else:
                cell = self.versions[version][_CELL_IDX]
                cytoplasm = self.versions[version][_CYTO_IDX]
                if IsVersion(cell):
                    cell = self.versions[cell][_CELL_IDX]
                if IsVersion(cytoplasm):
                    cytoplasm = self.versions[cytoplasm][_CYTO_IDX]
                output = nmpy.logical_xor(cell, cytoplasm)
        else:
            output = self.versions[version][compartment.value]
            if IsVersion(output):
                output = self.versions[output][compartment.value]

        return output

    def ClearBorderObjects(self) -> None:
        """"""
        if self.cytoplasm is None:
            originals = (self.cell,)
        else:
            originals = (self.cytoplasm, self.cell)
        new_version = [_cpt.copy() for _cpt in originals]

        # --- Clear outer segmentation border objects
        has_changed = _ClearBorderObjects(new_version, originals, -1)
        if more_than_1 := (new_version.__len__() > 1):
            # --- Clear inner segmentation border objects
            has_changed |= _ClearBorderObjects(new_version, originals, 0)

        cell = new_version[-1]
        if more_than_1:
            cytoplasm = new_version[0]
            has_changed = (has_changed, has_changed)
        else:
            cytoplasm = None
            has_changed = (has_changed, False)
        self._AddVersionForCompartments(cell, cytoplasm, "cleared borders", has_changed)

    def FilterCellsOut(
        self,
        CellIsInvalid: Callable[[int, array_t, dict], bool],
        /,
        **kwargs,
    ) -> None:
        """
        Currently, only applicable to the cell segmentation when no other compartments are present

        Parameters
        ----------
        CellIsInvalid: Arguments are: cell label (from 1), labeled segmentation, and (optional) keyword arguments
        kwargs: Passed to CellIsInvalid as keyword arguments

        Returns
        -------
        """
        assert self.cytoplasm is None

        compartment = self.cell.copy()

        labeled, n_cells = mrph.label(compartment, return_num=True, connectivity=1)
        invalids = []
        for label in range(1, n_cells + 1):
            if CellIsInvalid(label, labeled, **kwargs):
                invalids.append(label)

        if has_changed := (invalids.__len__() > 0):
            for label in invalids:
                compartment[labeled == label] = 0

        self._AddVersionForCompartments(
            compartment, self.cytoplasm, "filtered cells", (has_changed, False)
        )

    def CorrectBasedOnTemporalCoherence(
        self,
        previous: segmentation_t,
        /,
        *,
        min_jaccard: float = 0.75,
        max_area_discrepancy: float = 0.25,
    ) -> int:
        """
        min_jaccard: Actually, Pseudo-Jaccard

        Currently, only applicable to the cell segmentation when no other compartments are present
        """
        assert self.cytoplasm is None

        current = self.cell.copy()
        previous = previous.cell

        labeled_current, n_cells_current = mrph.label(
            current, return_num=True, connectivity=1
        )
        labeled_previous, n_cells_previous = mrph.label(
            previous, return_num=True, connectivity=1
        )
        jaccards = _PairwiseJaccards(
            n_cells_previous, n_cells_current, labeled_previous, labeled_current
        )
        c_to_p_links = _CurrentToPreviousLinks(jaccards, min_jaccard)

        n_corrections = 0
        for label_current in range(1, n_cells_current + 1):
            labels_previous = c_to_p_links.get(label_current - 1)
            if (labels_previous is not None) and (labels_previous.__len__() > 1):
                labels_previous = nmpy.array(labels_previous)
                labels_previous += 1

                where_fused = labeled_current == label_current

                seeds = _SeedsForSplitting(
                    where_fused,
                    label_current,
                    labeled_previous,
                    labels_previous,
                    max_area_discrepancy,
                )
                if seeds is None:
                    continue

                split = _WatershedBasedSplit(where_fused, seeds, labels_previous.size)
                if split is None:
                    continue

                current[where_fused] = 0
                current[split > 0] = 1
                n_corrections += 1

        self._AddVersionForCompartments(
            current,
            self.cytoplasm,
            "corrected w/ temp corr",
            (n_corrections > 0, False),
        )

        return n_corrections

    def AddFakeVersion(self, version: str, /) -> None:
        """"""
        self._AddVersionForCompartments(
            self.cell, self.cytoplasm, version, (False, False)
        )

    def _AddVersionForCompartments(
        self,
        cell: Union[array_t],
        cytoplasm: Union[array_t, None],
        version: str,
        has_changed: Tuple[bool, bool],
        /,
    ) -> None:
        """"""
        if has_changed[0]:
            self.cell = cell
        else:
            cell = self.version
        if has_changed[1]:
            self.cytoplasm = cytoplasm
        else:
            cytoplasm = self.version
        new_version = self._NewVersionFromCompartments(cell, cytoplasm)

        self.version_idx += 1
        self.version_name = version
        self.versions[self.version] = new_version

    def _NewVersionFromCompartments(
        self,
        cell: Union[array_t, version_id_h],
        cytoplasm: Union[array_t, None, version_id_h],
        /,
    ) -> version_h:
        """"""
        output = [None, None]

        if IsVersion(cell):
            cell = self._ActualOriginal(cell, _CELL_IDX)
        if IsVersion(cytoplasm):
            cytoplasm = self._ActualOriginal(cytoplasm, _CYTO_IDX)

        output[_CELL_IDX] = cell
        output[_CYTO_IDX] = cytoplasm

        return output[0], output[1]

    def _ActualOriginal(self, version: version_id_h, index: int, /) -> version_id_h:
        """"""
        output = version

        while IsVersion(self.versions[output][index]):
            output = self.versions[output][index]

        return output

    def AsDict(self) -> Dict[str, Any]:
        """"""
        output = {
            "cell": self.cell.tolist(),
            "cytoplasm": self.cytoplasm.tolist()
            if self.cytoplasm is not None
            else None,
            "version_idx": self.version_idx,
            "version_name": self.version_name,
            "versions": {},
        }

        versions = output["versions"]
        for name, values in self.versions.items():
            new_values = []
            for value in values:
                if (value is None) or IsVersion(value):
                    new_value = value
                else:
                    new_value = value.tolist()
                new_values.append(new_value)
            versions[name] = new_values

        return output


def IsVersion(maybe: Any, /) -> bool:
    """"""
    return (
        isinstance(maybe, tuple)
        and (maybe.__len__() == 2)
        and isinstance(maybe[0], int)
        and isinstance(maybe[1], str)
    )


def _ClearBorderObjects(
    compartments: List[array_t], originals: Sequence[array_t], idx: int, /
) -> bool:
    """"""
    compartment = compartments[idx]
    sgmt.clear_border(compartment, in_place=True)

    return not nmpy.array_equal(compartment, originals[idx])


def _PairwiseJaccards(
    n_cells_previous: int,
    n_cells_current: int,
    labeled_previous: array_t,
    labeled_current: array_t,
    /,
) -> array_t:
    """"""
    labels_previous = nmpy.fromiter(range(1, n_cells_previous + 1), dtype=nmpy.uint64)
    labels_current = nmpy.fromiter(range(1, n_cells_current + 1), dtype=nmpy.uint64)
    # Note the reversed parameter order in PseudoJaccard since a fusion is a division in reversed time
    _PseudoJaccard = lambda lbl_1, lbl_2: PseudoJaccard(
        labeled_current, labeled_previous, lbl_2, lbl_1
    )

    output = dstc.cdist(
        labels_previous[:, None], labels_current[:, None], metric=_PseudoJaccard
    )

    return output


def _CurrentToPreviousLinks(
    pairwise_jaccards: array_t, min_jaccard: float, /
) -> Dict[int, Sequence[int]]:
    """"""
    output = {}

    while True:
        row_idc, col_idc = spop.linear_sum_assignment(1.0 - pairwise_jaccards)
        valid_idc = pairwise_jaccards[row_idc, col_idc] > min_jaccard
        if not nmpy.any(valid_idc):
            break

        valid_row_idc = row_idc[valid_idc]
        for key, value in zip(col_idc[valid_idc], valid_row_idc):
            if key in output:
                output[key].append(value)
            else:
                output[key] = [value]

        pairwise_jaccards[valid_row_idc, :] = 0.0

    return output


def _SeedsForSplitting(
    where_fused: array_t,
    label_current: int,
    labeled_previous: array_t,
    labels_previous: array_t,
    max_area_discrepancy: float,
    /,
) -> Optional[array_t]:
    """"""
    output = nmpy.zeros_like(labeled_previous)

    for l_idx, previous_label in enumerate(labels_previous, start=1):
        output[labeled_previous == previous_label] = l_idx

    fused_area = nmpy.count_nonzero(where_fused)
    seeds_area = nmpy.count_nonzero(output)
    discrepancy = abs(seeds_area - fused_area) / fused_area
    if discrepancy > max_area_discrepancy:
        wrng.warn(
            f"Segmentation correction discarded due to high t-total-area/(t+1)-fused-area discrepancy "
            f"({discrepancy}) between cells {labels_previous} and fused cell {label_current}"
        )
        return None

    output[nmpy.logical_not(where_fused)] = 0
    # Just in case zeroing the non-fused region deleted some labels. If this can happen, it must be in very
    # pathological cases.
    output, *_ = sgmt.relabel_sequential(output)
    if (n_seeds := nmpy.amax(output)) != labels_previous.size:
        # Should never happen (see comment above)
        wrng.warn(
            f"Segmentation correction discarded due to invalid watershed seeds: "
            f"Actual={n_seeds}; Expected={labels_previous.size}"
        )
        return None

    return output


def _WatershedBasedSplit(
    where_fused: array_t, seeds: array_t, n_expected_regions: int, /
) -> Optional[array_t]:
    """"""
    distance_map = image_t.distance_transform_edt(where_fused)
    split = sgmt.watershed(
        -distance_map,
        seeds,
        connectivity=2,
        mask=where_fused,
        watershed_line=True,
    )

    split, n_split_regions = mrph.label(split > 0, return_num=True, connectivity=1)
    if n_split_regions > n_expected_regions:
        areas = []
        for split_label in range(1, n_split_regions + 1):
            area = sum(split == split_label)
            areas.append(area)
        ordered_labels = nmpy.argsort(areas) + 1
        n_too_many = n_split_regions - n_expected_regions
        for split_label in ordered_labels[:n_too_many]:
            split[split == split_label] = 0
        wrng.warn(
            f"Segmentation correction produced too many regions after watershed-based splitting: "
            f"Actual={n_split_regions}; Expected={n_expected_regions}\n"
            f"Keeping the {n_expected_regions} largest"
        )
    elif n_split_regions < n_expected_regions:
        wrng.warn(
            f"Segmentation correction discarded due to too few regions after watershed-based splitting: "
            f"Actual={n_split_regions}; Expected={n_expected_regions}"
        )
        return None

    return split
