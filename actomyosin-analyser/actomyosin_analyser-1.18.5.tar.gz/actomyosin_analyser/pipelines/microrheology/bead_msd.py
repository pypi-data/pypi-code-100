from typing import Tuple, List, Any, Union
import os
import json
import logging

import h5py
import matplotlib.pyplot as plt
import numpy as np
from .._pipeline import Pipeline
from ...tools.experiment_configuration import ExperimentConfiguration
from ...tools.experiment_iterator import Simulation, GroupIterator

logger = logging.getLogger(__name__)


class BeadMSD(Pipeline):

    def __init__(self, experiment_configuration: ExperimentConfiguration,
                 overwrite: bool=False):
        super().__init__(experiment_configuration)
        self.skip = experiment_configuration.skip_n_frames
        self.plot_files.update({
            'MSD': os.path.join(experiment_configuration['MSD'], 'ensemble_msds.svg'),
        })
        self.output_files.update({
            'MSD': os.path.join(experiment_configuration['MSD'], 'msd_ensemble.h5'),
        })

        if overwrite:
            self._remove_output_files()

    def run_analysis(self) -> Tuple[plt.Figure, plt.Axes]:
        msd_data = self.get_ensemble_msds()
        fig, ax = self._plot_msds(msd_data)
        return fig, ax

    def _validate_configuration(self):
        assert "MSD" in self.experiment_configuration

    def get_ensemble_msds(self) -> 'EnsembleMSDData':
        global_max = 0
        iterator = self.experiment_configuration.experiment_iterator
        data = EnsembleMSDData()
        for group in iterator:
            selected_simulations = [sim for sim in group]
            lag_time, msd_ensemble = self._get_ensemble_msds_group(group, selected_simulations)
            global_max = max(global_max, msd_ensemble.max())

            radius, bead_diffusion_const = self._load_bead_diffusion_const(selected_simulations[0])
            data.append_data(
                lag_time,
                msd_ensemble,
                radius,
                bead_diffusion_const,
                group.latex_label,
                group.color
            )
        return data

    def _plot_msds(self, data: 'EnsembleMSDData') -> Tuple[plt.Figure, plt.Axes]:
        filename = self.plot_files['MSD']
        fig, ax = data.plot(filename)
        return fig, ax

    def _load_bead_diffusion_const(self, sim: Simulation) -> Tuple[float, float]:
        init_idx = sim.data_reader.read_parameter('initial_state_index')
        format_string = BeadMSD._get_network_config_format_string(self.experiment_configuration.root_folder)
        init_config = format_string.format(init_idx)
        with open(init_config, 'rt') as fh:
            radius = json.load(fh)['acceptance_rate_handler']['bead_radius']
            bead_diffusion_const = 0.5 / radius
        return radius, bead_diffusion_const

    def _get_ensemble_msds_group(self, group: GroupIterator,
                                 selected_simulations) -> Tuple[np.ndarray, np.ndarray]:
        h5_group_template = group.get_label_from_values() + f"_skip_{self.skip}"
        h5_group_name = h5_group_template.format(**group.values)
        filename = self.output_files['MSD']
        lag_time, msd_ensemble = BeadMSD._load_ensemble_msds(filename, h5_group_name)
        if lag_time is not None:
            logger.info(f"Loaded MSD data of group {group.label} from file.")
            return lag_time, msd_ensemble

        logger.info(f"Computing MSD data of {group.label}, will save to file for next use.")
        lag_time, msds = self._get_individual_msds(selected_simulations)
        msd_ensemble = np.nanmean(msds, axis=0)
        BeadMSD._write_ensemble_msds(filename, h5_group_name, lag_time, msd_ensemble)
        return lag_time, msd_ensemble

    @staticmethod
    def _write_ensemble_msds(filename, h5_group_name, lag_time, msd_ensemble):
        with h5py.File(filename) as msds_file:
            h5_group = msds_file.create_group(h5_group_name)
            h5_group['log_msd'] = msd_ensemble
            h5_group['log_lag_time'] = lag_time

    @staticmethod
    def _load_ensemble_msds(
            filename: str,
            h5_group_name: str
    ) -> Union[Tuple[np.ndarray, np.ndarray], Tuple[None, None]]:
        if not os.path.exists(filename):
            return None, None
        with h5py.File(filename, 'r') as msds_file:
            if h5_group_name not in msds_file:
                return None, None
            h5_group = msds_file[h5_group_name]
            if 'log_msd' not in h5_group:
                return None, None
            return h5_group['log_lag_time'][:], h5_group['log_msd'][:]


    def _get_individual_msds(
            self, simulations: List[Simulation]
    ) -> Tuple[np.ndarray, np.ndarray]:
        lag_time = None
        msds = []
        for sim in simulations:
            dr = sim.data_reader
            a = sim.analyser
            msd_i = a.get_msd([0], non_filament=True, skip=self.skip)

            lags = msd_i[0, :, 0]
            msd_i = msd_i[0, :, 1]

            t_frames_steps = a.get_time_in_steps()
            dt = dr.read_dt() * (t_frames_steps[1] - t_frames_steps[0])
            if lag_time is None:
                lag_time = lags * dt
            else:
                assert (lag_time == lags * dt).all()
            msds.append(msd_i)
        return lag_time, np.vstack(msds)

    @staticmethod
    def _get_network_config_format_string(root_folder: str) -> str:
        for i in range(6):
            guessed_folder_name = os.path.join(root_folder, 'initial_states', f'network{"0"*i}')
            if os.path.exists(guessed_folder_name):
                return os.path.join(root_folder, 'initial_states', 'network{:0' + str(i) + '}',
                                    'config.json')
        raise RuntimeError("Unable to guess folder name of initial network, tried initial_states/"
                           "network0 to initial_states/network000000. This algorithm checks only for up to"
                           " 6 digits.")


class EnsembleMSDData:

    def __init__(self):
        self.lag_times = []
        self.msds = []
        self.bead_radii = []
        self.bead_diffusion_constants = []
        self.labels = []
        self.colors = []

    def append_data(self, lag_time, msd, bead_radius, bead_diffusion_constant, label, color):
        self.lag_times.append(lag_time)
        self.msds.append(msd)
        self.bead_radii.append(bead_radius)
        self.bead_diffusion_constants.append(bead_diffusion_constant)
        self.labels.append(label)
        self.colors.append(color)

    def get_lag_time_and_msd(self, index: int) -> Tuple[np.ndarray, np.ndarray]:
        return self.lag_times[index], self.msds[index]

    @property
    def length(self) -> int:
        return len(self.lag_times)

    def plot(self, filename: str) -> Tuple[plt.Figure, plt.Axes]:
        fig, ax = plt.subplots(1, 1)

        global_max = 0
        for i in range(self.length):
            msd = self.msds[i]
            global_max = max(global_max, msd.max())
            ax.plot(
                self.lag_times[i],
                msd,
                color=self.colors[i],
                label=self.labels[i]
            )
        colors, unique_free_diffusions = self._get_unique_free_diffusions()
        for i, (c, u) in enumerate(zip(colors, unique_free_diffusions)):
            label = 'free diff.' if i == 0 else None
            ax.plot(self.lag_times[i], u, '--', color=c,
                    label=label, zorder=1, alpha=0.7)

        ax.set(
            xscale='log',
            yscale='log',
            xlabel='lag time $\\tau / t_0$',
            ylabel='MSD $\\langle \\Delta r^2 \\rangle / x_0^2$',
        )
        # ax.legend(bbox_to_anchor=[1.05, 1.0], loc='upper left')
        ax.legend(
            loc='upper left', #bbox_to_anchor=(0.5, 1.05),
            ncol=2
        )
        ylim = ax.get_ylim()
        ax.set_ylim(ylim[0], global_max * 1.2)
        fig.tight_layout()
        fig.savefig(filename)
        return fig, ax

    def _get_unique_free_diffusions(self) -> Tuple[List[Any], List[np.ndarray]]:
        diff_consts = np.array(self.bead_diffusion_constants)
        uniques = np.unique(diff_consts)
        if len(uniques) == 1:
            return ['black'], [6 * self.lag_times[0] * uniques[0]]
        elif len(uniques) == self.length:
            return (self.colors,
                    [6 * self.lag_times[i] * self.bead_diffusion_constants[i] for i in range(self.length)])
        raise RuntimeError("Can only handle cases where all beads have same size or all beads have different size."
                           f" Your experiment has {self.length} ensemble MSDs "
                           f"and {len(uniques)} different bead sizes.")
