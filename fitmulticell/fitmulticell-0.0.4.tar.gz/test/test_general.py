import pyabc
import fitmulticell as fmc
import os
import numpy as np
import tempfile


def test_nothing():
    pass


def _test_mapk():
    """
    Just runs an analysis with the MAPK model to ensure that at least
    not execution errors occur.
    """
    file_ = "doc/example/MAPK_SBML.xml"
    par_map = {'V1': './CellTypes/CellType/System/Constant[@symbol="V1"]',
               'V2': './CellTypes/CellType/System/Constant[@symbol="V2"]',
               'k3': './CellTypes/CellType/System/Constant[@symbol="k3"]'}

    model = fmc.model.MorpheusModel(
        file_, par_map=par_map,
        # executable="ch-run ../../test/morpheus_docker -- /usr/bin/morpheus",
        show_stdout=False, show_stderr=True,
        raise_on_error=False)

    true_pars = {'V1': 2.7, 'V2': 0.25, 'k3': 0.025}
    limits = {key: (0.5 * val, 2 * val) for key, val in true_pars.items()}

    # generate data
    observed_data = model.sample(true_pars)

    prior = pyabc.Distribution(**{key: pyabc.RV("uniform", lb, ub - lb)
                                  for key, (lb, ub) in limits.items()})

    def distance(val1, val2):
        d = np.sum([np.sum(np.abs(val1[key] - val2[key]))
                    for key in ['IdSumstat__MAPK_P', 'IdSumstat__MKK_P']])
        return d

    abc = pyabc.ABCSMC(model, prior, distance, population_size=5)
    db_path = "sqlite:///" + os.path.join(tempfile.gettempdir(), "test.db")
    abc.new(db_path, observed_data)

    # run
    h = abc.run(max_nr_populations=3)

    pyabc.visualization.plot_epsilons(h)
    df, w = h.get_distribution(t=h.max_t)
    pyabc.visualization.plot_kde_matrix(
        df, w, limits=limits, refval=true_pars)
