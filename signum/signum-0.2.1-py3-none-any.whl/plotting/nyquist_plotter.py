import numpy as np
import matplotlib.pyplot as plt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from signum import SignalContainer

from signum.plotting.plotter import Plotter


class NyquistPlotter(Plotter):
    def __init__(self, figsize=(6, 6), **kwargs):
        super().__init__(n_rows=1, n_cols=1, figsize=figsize, **kwargs)

        self.ax.set_xlabel("I component")
        self.ax.set_ylabel("Q component")
        self.ax.set_aspect("equal")
        self.ax.axvline(0, color='k', zorder=1)
        self.ax.axhline(0, color='k', zorder=1)

    @property
    def ax(self) -> plt.Axes:
        return self.axes[0, 0]

    def _add_line(self, signal: 'SignalContainer', set_equal_limits=True, **kwargs):
        line, = self.ax.plot(signal.real.T, signal.imag.T, **kwargs)

        self.ax.relim()

        if set_equal_limits:
            lim = np.max(np.abs([*self.ax.get_xlim(), *self.ax.get_ylim()]))
            self.ax.set_xlim(-lim, lim)
            self.ax.set_ylim(-lim, lim)

        return line,
