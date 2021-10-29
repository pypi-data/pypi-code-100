# data.py
""" Data to used alongside the test suite """

from src.udmis.typings import UDMISConfiguration


udmis_graph = [(0.3461717838632017, 1.4984640297338632),
               (0.6316400411846113, 2.5754677320579895),
               (1.3906262250927481, 2.164978861396621),
               (0.66436005100802, 0.6717919819739032),
               (0.8663329771713457, 3.3876341010035995),
               (1.1643107343501296, 1.0823066243402013)
               ]

udmis_polynomial_coefficients = [0.1, 0.1, 0.1, 0.1, 0.1]

udmis_test_configurations = [
    {
        'graph': udmis_graph,
        'n_qubits': len(udmis_graph),
        'instance': 1,
        'max_schedule_time': 50,
        'time_interval': 1e-2,
        'solver': 'exp',
        'plot_energy_and_gap': True,
        'use_full_hamiltonian': True,
    },
    {
        'graph': udmis_graph,
        'n_qubits': len(udmis_graph),
        'instance': 1,
        'max_schedule_time': 50,
        'time_interval': 1e-2,
        'solver': 'exp',
        'plot_energy_and_gap': True,
        'use_full_hamiltonian': True,
        'polynomial_coefficients': udmis_polynomial_coefficients,
        'scheduling_optimization_method': 'linear',
        'max_iter': 10000,
    },
]


udmis_bad_test_configurations = [
    UDMISConfiguration({}),
    UDMISConfiguration({
        'graph': udmis_graph,
    }),
    UDMISConfiguration({
        'graph': udmis_graph,
        'n_qubits': len(udmis_graph),
    }),
    UDMISConfiguration({
        'graph': udmis_graph,
        'n_qubits': len(udmis_graph),
        'instance': 1,
    })
]

udmis_configurations = [
    UDMISConfiguration({
        'graph': udmis_graph,
        'n_qubits': len(udmis_graph),
        'instance': 1,
        'max_schedule_time': 50,
        'time_interval': 1e-2,
        'solver': 'exp',
        'plot_energy_and_gap': False,
        'use_full_hamiltonian': True,
    }),
]
