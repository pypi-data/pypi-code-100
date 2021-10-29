from copy import deepcopy
from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
import numpy as np

if TYPE_CHECKING:
    from signum import SignalContainer

from signum.tools.scale_manager import ScaleManager


class Plotter:
    def __init__(self, n_rows=1, n_cols=1, title=None, unit=None, x_unit=None, **kwargs):
        fig, axes = plt.subplots(n_rows, n_cols, **kwargs)
        if n_rows == 1 and n_cols == 1:
            axes = np.array([axes])
        axes = axes.reshape(n_rows, n_cols)

        self.fig = fig
        self.axes = axes
        self.lines = {}
        self.plot_data = {}
        self._unit = unit
        self._x_unit = x_unit

        self.x_description = ''
        self.y_description = ''

        if title:
            fig.suptitle(title)

        for ax in axes.flatten():
            ax.grid(color='lightgrey')

    @property
    def x_unit_bracket(self):
        return f"[{self._x_unit}]" if self._x_unit else ''

    @property
    def unit_bracket(self):
        return f"[{self._unit}]" if self._unit else ''

    def add_legend(self, **kwargs):
        """Add legend to each of the main grid axes."""

        for ax in self.axes.flatten():
            ax.legend(fancybox=True, framealpha=0.5, **kwargs)

    def show_fig(self, **kwargs):
        self.fig.show(**kwargs)

    @staticmethod
    def show_all(**kwargs):
        plt.show(**kwargs)

    def _fix_units(self, signal):
        if self._unit and signal.unit and self._unit != signal.unit:
            _, own_unit_core = ScaleManager.split_unit(self._unit)
            _, signal_unit_core = ScaleManager.split_unit(signal.unit)
            if own_unit_core != signal_unit_core:
                raise ValueError(f"Signal unit: '{signal.unit}' does not match plot unit: '{self._unit}'")
            order_change = ScaleManager.order_from_unit(self._unit) - ScaleManager.order_from_unit(signal.unit)
            signal, new_unit = ScaleManager.rescale(signal, signal.unit, order_change)
            signal.unit = new_unit

        if self._x_unit and signal.x_unit and self._x_unit != signal.unit:
            _, own_x_unit_core = ScaleManager.split_unit(self._x_unit)
            _, signal_x_unit_core = ScaleManager.split_unit(signal.x_unit)
            if own_x_unit_core != signal_x_unit_core:
                raise ValueError(f"Signal x unit: '{signal.x_unit}' does not match plot x unit: '{self._x_unit}'")
            order_change = ScaleManager.order_from_unit(self._x_unit) - ScaleManager.order_from_unit(signal.x_unit)
            x_axis, new_unit = ScaleManager.rescale(signal.x_axis, signal.x_unit, order_change)
            signal = deepcopy(signal)
            signal.x_axis = x_axis
            signal.x_unit = new_unit

        self._unit = self._unit or signal.unit
        self._x_unit = self._x_unit or signal.x_unit
        self.x_description = self.x_description or signal.x_description

        return signal

    def _update_labels(self):
        pass

    def add_line(self, signal: 'SignalContainer', add_legend=True, **kwargs):
        signal = self._fix_units(signal)

        if signal.description and 'label' not in kwargs:
            kwargs['label'] = signal.description

        lines = self._add_line(signal, **kwargs)

        if add_legend and 'label' in kwargs:
            self.add_legend()

        k = kwargs.get('label', f'line {len(self.lines)}')
        self.lines[k] = lines
        self.plot_data[k] = signal

        self._update_labels()

    def _add_line(self, signal, **kwargs):
        raise NotImplementedError


class SimplePlotter(Plotter):
    def __init__(self, x_label='', y_label='', **kwargs):
        super().__init__(n_rows=1, n_cols=1, **kwargs)

        self.x_description = x_label
        self.y_description = y_label
        self._update_labels()

    @property
    def ax(self):
        return self.axes[0, 0]

    def _add_line(self, signal: 'SignalContainer', **kwargs):
        if np.iscomplexobj(signal):
            raise ValueError("Can't plot complex data on a SimplePlotter")

        line, = self.ax.plot(signal.x_axis, signal, **kwargs)

        return line,

    def _update_labels(self):
        self.ax.set_xlabel(f"{self.x_description} {self.x_unit_bracket}")
        self.ax.set_ylabel(f"{self.y_description} {self.unit_bracket}")
