""" Typings from UD-MIS module """
from typing import TypedDict, Tuple, List


class UDMISConfiguration(TypedDict, total=False):
    """ UDMIS Configuration dictionary
        Args:
            n_qubits (int): number of qubits for the file that contains the
                information of an Exact Cover instance.
            instance (int): intance used for the desired number of qubits.
            max_schedule_time (float): maximum schedule time. The larger, better final results.
            time_interval (float): time interval for the evolution.
            solver (str): solver used for the adiabatic evolution.
            plot_energy_and_gap (bool): decides if plots of the energy and gap will be returned.
            use_full_hamiltonian (bool): decides if the full Hamiltonian matrix will be used.
            polynomial_coefficients (list): list of polynomial coefficients for scheduling function.
                Default is linear scheduling.
            scheduling_optimization_method (str): Method to use for scheduling optimization (optional).
            max_iter (int): Maximum iterations for scheduling optimization (optional)
    """
    graph: List[Tuple[float, float]]
    n_qubits: int
    instance: int
    max_schedule_time: float
    time_interval: float
    solver: str
    plot_energy_and_gap: bool
    use_full_hamiltonian: bool
    polynomial_coefficients: List[float]
    scheduling_optimization_method: str
    max_iter: int


class UDMISSolution(TypedDict):
    solution: str
    probability: float
