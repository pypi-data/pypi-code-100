import matplotlib.pyplot as plt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from signum import SignalContainer

from signum.plotting.plotter import Plotter


class PolarPlotter(Plotter):
    def __init__(self, figsize=(6, 6), db_scale=False, **kwargs):
        super().__init__(n_rows=1, n_cols=1, figsize=figsize, subplot_kw={'projection': 'polar'}, **kwargs)

        self._db_scale = db_scale

        self.ax.grid(color='lightgrey')

    @property
    def ax(self) -> plt.Axes:
        return self.axes[0, 0]

    def _add_line(self, signal: 'SignalContainer', set_equal_limits=True, **kwargs):
        mag = signal.magnitude_db if self._db_scale else signal.magnitude
        phase = signal.get_phase(rad=True)

        line, = self.ax.plot(phase.T, mag.T, **kwargs)

        return line,
