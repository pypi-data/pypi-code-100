import matplotlib.pyplot as plt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from signum import SignalContainer

from signum.plotting.plotter import Plotter


class IQPlotter(Plotter):
    def __init__(self, figsize=(8, 6), sharey='all', **kwargs):
        super().__init__(n_rows=2, n_cols=1, sharex='all', sharey=sharey, figsize=figsize, **kwargs)

        self.i_ax.set_ylabel("Real")
        self.q_ax.set_ylabel("Imag")

    @property
    def i_ax(self) -> plt.Axes:
        return self.axes[0, 0]

    @property
    def q_ax(self) -> plt.Axes:
        return self.axes[1, 0]

    def _add_line(self, signal: 'SignalContainer', **kwargs):
        i_line, = self.i_ax.plot(signal.x_axis, signal.real.T, **kwargs)
        q_line, = self.q_ax.plot(signal.x_axis, signal.imag.T, **kwargs)

        return i_line, q_line

    def _update_labels(self):
        self.i_ax.set_ylabel(f"Real {self.unit_bracket}")
        self.q_ax.set_ylabel(f"Imag {self.unit_bracket}")
        self.q_ax.set_xlabel(f"{self.x_description} {self.x_unit_bracket}")

