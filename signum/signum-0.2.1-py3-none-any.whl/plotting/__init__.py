import numpy as np

from signum.plotting.bode_plotter import BodePlotter
from signum.plotting.iq_plotter import IQPlotter
from signum.plotting.nyquist_plotter import NyquistPlotter
from signum.plotting.plotter import Plotter, SimplePlotter
from signum.plotting.polar_plotter import PolarPlotter

complex_plotters = {
    'bode': BodePlotter,
    'iq': IQPlotter,
    'nyquist': NyquistPlotter,
    'polar': PolarPlotter
}

plotters = {
    'simple': SimplePlotter,
    **complex_plotters
}


def get_plotter_class(plotter_type, complex_only=False):
    plotter_dict = complex_plotters if complex_only else plotters

    if plotter_type in plotter_dict:
        return plotter_dict[plotter_type]

    plotter_names = list(plotter_dict.keys())
    raise ValueError(f"Unknown {'complex ' if complex_only else ''}plotter type: '{plotter_type}'; "
                     f"choose from: {plotter_names}")


def get_plotter(plotter_type, complex_only=False, **kwargs):
    return get_plotter_class(plotter_type, complex_only=complex_only)(**kwargs)


def plot_signal(signal, plot_type: str = None, show: bool = True, title: str = None, plot_kwargs=None, **kwargs):
    if signal.size < 2:
        kwargs['marker'] = kwargs.get('marker', 'o')  # put a single dot if there is only one data point

    is_complex = np.iscomplexobj(signal)
    if plot_type is None:
        plot_type = 'bode' if is_complex else 'simple'
    ptr = get_plotter(plot_type, complex_only=is_complex, title=title, **(plot_kwargs or {}))

    ptr.add_line(signal, **kwargs)

    if show:
        ptr.show_fig()

    return ptr
