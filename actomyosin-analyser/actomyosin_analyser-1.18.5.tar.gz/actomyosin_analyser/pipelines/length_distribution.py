import logging
import os
from multiprocessing import Pool
from typing import List, Tuple, Union

import h5py
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

from ._pipeline import Pipeline
from ..tools.experiment_configuration import ExperimentConfiguration
from ..tools.experiment_iterator import GroupIterator, Simulation
from ..analysis import geometry

logger = logging.getLogger(__name__)
_KDE_XY_Pair = Tuple[np.ndarray, np.ndarray]


class LengthDistribution(Pipeline):

    def _validate_configuration(self):
        assert "SegmentLength" in self.experiment_configuration

    def __init__(self, experiment_configuration: ExperimentConfiguration,
                 n_processes: int=1):
        super().__init__(experiment_configuration)
        self._n_processes = n_processes

        self.plot_files.update({
            "length_distributions": os.path.join(experiment_configuration["SegmentLength"],
                                                 'length_distributions_{frames}.svg')
        })
        self.output_files.update({
            "length_distributions": os.path.join(experiment_configuration["SegmentLength"],
                                                 'length_distributions.h5')
        })

    def run_analysis(self, n_points_kde: int,
                     frames: List[int]):
        density_estimates_list = self.get_density_estimates(n_points_kde, frames)
        fig, ax = plt.subplots(len(frames), 1, sharex=True)
        self.plot_density_estimates(ax, density_estimates_list, frames)
        fig.savefig(self.plot_files["length_distributions"].format(
            frames='_'.join([str(f) for f in frames])
        ))

    def plot_density_estimates(self, ax, density_estimates: List[List[_KDE_XY_Pair]],
                               frames: List[int]):
        for i, f in enumerate(frames):
            self._plot_distributions_single_frame(ax[i], density_estimates[i])
            if i == 0:
                ax[i].legend()
            ax[i].set(
                title=f'frame {f}',
                ylabel='density',
            )
            if i + 1 == len(frames):
                ax[i].set_xlabel('segment length / $x_0$')

    def get_density_estimates(
            self,
            n_points_kde: int,
            frames: List[int]
    ) -> List[List[_KDE_XY_Pair]]:

        result_xy_pairs = []
        for f in frames:
            result_xy_pairs.append(self._get_density_estimates_single_frame(n_points_kde, f))

        return result_xy_pairs

    def _get_density_estimates_single_frame(
            self,
            n_points_kde: int,
            frame: int
    ) -> List[_KDE_XY_Pair]:
        iterator = self.experiment_configuration.experiment_iterator
        result_xy_pairs = []
        for group in iterator:
            x, density_estimate = self._get_density_estimates_single_group(group, n_points_kde, frame)
            result_xy_pairs.append((x, density_estimate))

        return result_xy_pairs

    def _get_density_estimates_single_group(
            self,
            group: GroupIterator,
            n_points_kde: int,
            frame: int
    ) -> _KDE_XY_Pair:

        label = group.get_label_from_values()
        x, density_estimate = self._load_density_estimate(label, n_points_kde, frame)
        if x is not None:
            return x, density_estimate
        x, density_estimate = self._compute_density_estimate(group, n_points_kde, frame)
        self._save_density_estimate(x, density_estimate,
                                    label, n_points_kde, frame)
        return x, density_estimate


    def _load_density_estimate(
            self,
            label: str,
            n_points_kde: int,
            frame: int
    ) -> Union[_KDE_XY_Pair, Tuple[None, None]]:
        fname = self.output_files["length_distributions"]
        if not os.path.exists(fname):
            return None, None

        with h5py.File(fname, 'r') as file:
            if label not in file:
                return None, None
            g = file[label]
            if str(frame) not in g:
                return None, None
            gg = g[str(frame)]
            if str(n_points_kde) not in gg:
                return None, None
            ggg = gg[str(n_points_kde)]

            x = ggg['x'][:]
            de = ggg['density_estimate'][:]
            return x, de

    def _compute_density_estimate(
            self,
            group: GroupIterator,
            n_points_kde: int,
            frame: int
    ) -> _KDE_XY_Pair:
        selected_simulations = [sim for sim in group]
        lengths = self.get_lengths(selected_simulations, frame)
        logger.warning("Saving lengths to lengths.npy, this is a debugging add-on."
                       " Remove it when bug is resolved!!")
        np.save('lengths.npy', lengths)
        kde = gaussian_kde(lengths)
        x = np.linspace(lengths.min(), lengths.max(), n_points_kde)
        return x, kde(x)

    def get_lengths(
            self,
            selected_simulations: List[Simulation],
            frame: int
    ) -> np.ndarray:
        pool = Pool(self._n_processes)

        caller = _GetLengthsCaller(frame)

        lengths = pool.map(
            caller,
            selected_simulations
        )

        lengths = np.concatenate(lengths).flatten()
        return lengths

    def _save_density_estimate(
            self,
            x: np.ndarray,
            density_estimate: np.ndarray,
            label: str,
            n_points_kde: int,
            frame: int
    ):
        fname = self.output_files["length_distributions"]
        with h5py.File(fname, 'a') as file:
            if label in file:
                g = file[label]
            else:
                g = file.create_group(label)
            if str(frame) in g:
                gg = g[str(frame)]
            else:
                gg = g.create_group(str(frame))
            if str(n_points_kde) in gg:
                ggg = gg[str(n_points_kde)]
            else:
                ggg = gg.create_group(str(n_points_kde))

            ggg['x'] = x
            ggg['density_estimate'] = density_estimate

    def _plot_distributions_single_frame(
            self,
            ax: plt.Axes,
            density_estimate_pairs: List[_KDE_XY_Pair]
    ):
        iterator = self.experiment_configuration.experiment_iterator
        for i, group in enumerate(iterator):
            x, estimate = density_estimate_pairs[i]
            ax.plot(x, estimate, label=group.latex_label, color=group.color)


class _GetLengthsCaller:

    def __init__(self, frame: int):
        self.frame = frame

    def __call__(self, sim: Simulation) -> np.ndarray:
        return self._get_lengths_single_simulation(sim)

    def _get_lengths_single_simulation(
            self,
            simulation: Simulation
    ) -> np.ndarray:
        lengths = []
        coords = simulation.analyser.get_trajectories_filaments()[self.frame]
        filaments = simulation.analyser.get_filaments()[self.frame]

        box = simulation.analyser.data_reader.read_box_size()
        box = np.array([box[1, 0] - box[0, 0],
                        box[1, 1] - box[0, 1],
                        box[1, 2] - box[0, 2]])

        for f in filaments:
            fcoords = coords[f.items]
            v_segments = geometry.get_minimum_image_vector(
                fcoords[:-1], fcoords[1:], box)
            d = np.sqrt(np.sum(v_segments ** 2, 1))
            lengths.append(d)
        return np.array(lengths)
