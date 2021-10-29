import matplotlib.pyplot as plt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from signum import SignalContainer

from signum.plotting.plotter import Plotter


class BodePlotter(Plotter):
    def __init__(self, figsize=(8, 6), db_scale: bool = False, rad: bool = False, unwrapped: bool = False, **kwargs):
        super().__init__(n_rows=2, n_cols=1, sharex='all', figsize=figsize, **kwargs)

        self.amplitude_ax.set_ylabel(f"Amplitude{' [db]' if db_scale else ''}")
        self.phase_ax.set_ylabel(f"Phase [{'rad' if rad else 'deg'}]")

        self._db_scale = db_scale
        self._rad = rad
        self._unwrapped = unwrapped

    @property
    def amplitude_ax(self) -> plt.Axes:
        return self.axes[0, 0]

    @property
    def phase_ax(self) -> plt.Axes:
        return self.axes[1, 0]

    def _add_line(self, signal: 'SignalContainer', **kwargs):
        mag = signal.magnitude_db if self._db_scale else signal.magnitude
        amplitude_line, = self.amplitude_ax.plot(signal.x_axis, mag.T, **kwargs)

        phase = signal.get_phase(rad=self._rad, unwrapped=self._unwrapped)
        phase_line, = self.phase_ax.plot(signal.x_axis, phase.T, **kwargs)

        return amplitude_line, phase_line

    def _update_labels(self):
        self.amplitude_ax.set_ylabel(f"Amplitude {'[db]' if self._db_scale else self.unit_bracket}")
        self.phase_ax.set_xlabel(f"{self.x_description} {self.x_unit_bracket}")

