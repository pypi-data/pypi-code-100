from abc import ABC
from typing import List, Tuple
from .typings import UDMISConfiguration, UDMISSolution
import time
import numpy as np
from qibo import hamiltonians, models, callbacks, matrices, symbols, K
from .plot_aux import plot_energy, plot_graph


class UDMIS(ABC):
    """ Implements Unit-Disk Maximum Independent Set (UD-MIS) problem. """

    def __init__(self, configuration: UDMISConfiguration):
        """ Initialize the UDMIS configuration class
            Args:
              configuration: UDMIS configuration dictionary
        """
        self._graph = configuration['graph']
        self._n_qubits = configuration['n_qubits']
        self._instance = configuration['instance']
        self._max_schedule_time = configuration['max_schedule_time']
        self._time_interval = configuration['time_interval']
        self._solver = configuration['solver']
        self._plot_energy_and_gap = configuration['plot_energy_and_gap']
        self._use_full_hamiltonian = configuration['use_full_hamiltonian']

        self._polynomial_coefficients = (
            configuration['polynomial_coefficients'] if 'polynomial_coefficients' in configuration else None)
        self._scheduling_optimization_method = (
            configuration['scheduling_optimization_method'] if 'scheduling_optimization_method' in configuration
            else None)
        self._max_iter = configuration['max_iter'] if 'max_iter' in configuration else None

        self._edges_list = self._get_edges()

        self._set_hamiltonians()
        self._check_if_possible_to_plot_energy_and_gap()
        self._set_scheduling_function()
        self._set_adiabiatic_evolution()
        self._setup_optimization_schedule()

    def optimize(self) -> UDMISSolution:
        """ Executes the UD-MIS problem with the specified configuration.
            Adiabatic evoluition to find the solution of an exact cover instance

            Returns:
              Result of the most probable outcome after the adiabatic evolution.
              Plots of the ground and excited state energies and the underlying gap
              during the adiabatic evolution. The plots are created only if the
              ``plot_energy_and_gap`` option is enabled.
        """
        start_time = time.time()

        initial_state = np.ones(2 ** self._n_qubits) / np.sqrt(2 ** self._n_qubits)
        final_state = self._adiabatic_evolution(final_time=self._max_schedule_time, initial_state=initial_state)

        output_dec = (np.abs(K.to_numpy(final_state))**2).argmax()
        max_output = "{0:0{bits}b}".format(output_dec, bits=self._n_qubits)
        max_prob = (np.abs(K.to_numpy(final_state))**2).max()

        print("Exact cover instance with {} qubits.\n".format(self._n_qubits))

        print('-' * 20 + '\n')
        print(f'Adiabatic evolution with total time {self._max_schedule_time}, evolution step {self._time_interval} '
              f'and solver {self._solver}.\n')
        print(f'Most common solution after adiabatic evolution: {max_output}.\n')
        print(f'Found with probability: {max_prob}.\n')
        if self._plot_energy_and_gap:
            print('-' * 20 + '\n')
            plot_energy(self._n_qubits,
                        self._ground[:],
                        self._excited[:],
                        self._gap[:],
                        self._time_interval,
                        self._max_schedule_time)
            plot_graph(self._graph, self._edges_list, max_output, self._n_qubits)
            print('Plots finished.\n')
        print(f'Execution time: {time.time()-start_time} seconds')
        return UDMISSolution({
            'solution': max_output,
            'probability': max_prob
        })

    def _setup_optimization_schedule(self):
        if self._scheduling_optimization_method is not None:
            print(f'Optimizing scheduling using {self._scheduling_optimization_method}.\n')
            if self._polynomial_coefficients is None:
                self._polynomial_coefficients = [self._max_schedule_time]
            else:
                self._polynomial_coefficients.append(self._max_schedule_time)
            if self._scheduling_optimization_method == "sgd":
                options = {"nepochs": self._max_iter}
            else:
                options = {"maxiter": self._max_iter, "disp": True}
            energy, params, _ = self._adiabatic_evolution.minimize(self._polynomial_coefficients,
                                                                   method=self._scheduling_optimization_method,
                                                                   options=options)
            self._max_schedule_time = params[-1]

    def _set_adiabiatic_evolution(self):
        # Define evolution model and (optionally) callbacks
        if self._plot_energy_and_gap:
            self._ground = callbacks.Gap(0)
            self._excited = callbacks.Gap(1)
            self._gap = callbacks.Gap()
            self._adiabatic_evolution = models.AdiabaticEvolution(self._H0,
                                                                  self._H1,
                                                                  self._scheduling_function,
                                                                  self._time_interval,
                                                                  solver=self._solver,
                                                                  callbacks=[self._gap, self._ground, self._excited])
        else:
            self._adiabatic_evolution = models.AdiabaticEvolution(
                self._H0, self._H1, self._scheduling_function, self._time_interval, solver=self._solver)

    def _set_scheduling_function(self):
        # Define scheduling according to given params
        if self._polynomial_coefficients is None:
            # default is linear scheduling
            def s(t):
                return t
        else:
            if self._scheduling_optimization_method is None:
                def s(t):
                    return self._spolynomial(t, self._polynomial_coefficients)
            else:
                s = self._spolynomial
        self._scheduling_function = s

    def _check_if_possible_to_plot_energy_and_gap(self):
        if self._plot_energy_and_gap and self._n_qubits >= 14:
            print('Currently not possible to calculate gap energy for {} qubits.'
                  '\n Proceeding to adiabatic evolution without plotting data.\n'
                  ''.format(self._n_qubits))
            self._plot_energy_and_gap = False
        if self._plot_energy_and_gap and self._scheduling_optimization_method is not None:
            print('Not possible to calculate gap energy during optimization.')
            self._plot_energy_and_gap = False

    def _get_edges(self) -> List[Tuple[int, int]]:
        num_vertices = len(self._graph)
        r = 1
        edges_list = []

        for i in range(num_vertices):
            for j in range(i + 1, num_vertices):
                if np.linalg.norm(np.subtract(self._graph[i], self._graph[j])) < r:
                    edges_list.append((i, j))

        return edges_list

    def _h_problem(self, edges_list: List[Tuple[int, int]]):
        """Hamiltonian that satisfies all Exact Cover clauses.
        Args:
            qubits (int): # of total qubits in the instance.
            edges_list (list): list of tuples with the vertices connected by the edges.
        Returns:
            sham (sympy.Expr): Symbolic form of the problem Hamiltonian.
            smap (dict): Dictionary that maps the symbols that appear in the
                Hamiltonian to the corresponding matrices and target qubits.
        """
        u = 1.35
        z_matrix = (matrices.I - matrices.Z) / 2.0
        z = [symbols.Symbol(i, z_matrix) for i in range(self._n_qubits)]
        return (-sum(z[i] for i in range(self._n_qubits)) + u * sum(z[i] * z[j] for i, j in edges_list))

    def _h_initial(self):
        """Initial hamiltonian for adiabatic evolution.
        Args:
            qubits (int): # of total qubits in the instance.
        Returns:
            sham (sympy.Expr): Symbolic form of the easy Hamiltonian.
            smap (dict): Dictionary that maps the symbols that appear in the
                Hamiltonian to the corresponding matrices and target qubits.
        """
        return sum(0.5 * (1 - symbols.X(i)) for i in range(self._n_qubits))

    def _spolynomial(self, t):
        """General polynomial scheduling satisfying s(0)=0 and s(1)=1."""
        f = sum(p * t ** (i + 2) for i, p in enumerate(self._polynomial_coefficients))
        f += (1 - np.sum(self._polynomial_coefficients)) * t
        return f

    def _ground_state(self):
        """Returns |++...+> state to be used as the ground state of the easy Hamiltonian."""
        return K.cast(np.ones(2 ** self._n_qubits) / np.sqrt(2 ** self._n_qubits))

    def _set_hamiltonians(self):
        # Define "easy" and "problem" Hamiltonians
        self._easy_hamiltonian = self._h_initial()
        self._problem_hamiltonian = self._h_problem(self._edges_list)

        self._H0 = hamiltonians.SymbolicHamiltonian(self._easy_hamiltonian, ground_state=self._ground_state())
        self._H1 = hamiltonians.SymbolicHamiltonian(self._problem_hamiltonian)

        if self._use_full_hamiltonian:
            print('Using the full Hamiltonian evolution\n')
            self._H0, self._H1 = self._H0.dense, self._H1.dense
        else:
            print('Using Trotter decomposition for the Hamiltonian\n')
