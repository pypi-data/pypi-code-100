""" Test methods for ud-mis.py """
import pytest
from src.udmis import UDMIS, UDMISConfiguration
from .data import udmis_test_configurations, udmis_bad_test_configurations, udmis_configurations
import numpy as np


@pytest.mark.parametrize("udmis_test_configuration", udmis_test_configurations)
def test_udmis_construction(udmis_test_configuration):
    udmis_configuration = UDMISConfiguration({
        'graph': udmis_test_configuration['graph'],
        'n_qubits': udmis_test_configuration['n_qubits'],
        'instance': udmis_test_configuration['instance'],
        'max_schedule_time': udmis_test_configuration['max_schedule_time'],
        'time_interval': udmis_test_configuration['time_interval'],
        'solver': udmis_test_configuration['solver'],
        'plot_energy_and_gap': udmis_test_configuration['plot_energy_and_gap'],
        'use_full_hamiltonian': udmis_test_configuration['use_full_hamiltonian'],
    })
    udmis = UDMIS(configuration=udmis_configuration)
    assert isinstance(udmis, UDMIS)


@pytest.mark.parametrize("udmis_bad_test_configuration", udmis_bad_test_configurations)
def test_udmis_bad_construction(udmis_bad_test_configuration):
    with pytest.raises(KeyError):
        UDMIS(configuration=udmis_bad_test_configuration)


@pytest.mark.parametrize("udmis_configuration", udmis_configurations)
def test_udmis_optimize(udmis_configuration):
    udmis = UDMIS(configuration=udmis_configuration)
    result = udmis.optimize()
    assert result['solution'] == '001011'
    assert np.round(result['probability'], 4) == np.round(0.31936156736264204, 4)
