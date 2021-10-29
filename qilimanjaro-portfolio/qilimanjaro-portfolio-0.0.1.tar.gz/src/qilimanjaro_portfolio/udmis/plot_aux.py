# plot_aux.py
# Auxiliary functions for plotting
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np


def circle(pos, r, color):
    """Draw a circle in the current plot
    Args:
        pos (tuple): Position (x,y) of the circle's center.
        r (float): radius of the circle.
        color (string): background color for the circle.
        """
    ax = plt.gca()
    c = Circle(xy=pos, radius=r)
    ax.add_artist(c)

    c.set_clip_box(ax.bbox)
    c.set_edgecolor('black')
    c.set_facecolor(color)
    c.set_alpha(0.3)


def plot_graph(graph, edges_list, solution, n_qubits):
    """Shows the graph of the problem with the solution
    Args:
        graph (list): list of tuples (x,y) containing the position of the graph vertices.
        edges (list): list of tuples (i,j) with the vertices i,j connected by an edge.
        solution (list/str): list or string with the values 0/1 for every vertex.
    Returns:
        solution_graph.png: graph where the red vertices are the solution of the UD-MIS problem.
    """
    color_list = []
    for i, v in enumerate(graph):
        if str(solution[i]) == '0':
            color_list.append('black')
            color = 'lightgray'
        elif str(solution[i]) == '1':
            color_list.append('red')
            color = 'salmon'

        circle(v, 0.5, color)

    plt.scatter(*zip(*graph), color=color_list)

    for i, j in edges_list:
        plt.plot(*zip(graph[i], graph[j]), c="blue")

    plt.margins(0.25)
    plt.axis('equal')
    plt.savefig('images/{}_solution_graph.png'.format(n_qubits), dpi=300, bbox_inches='tight')
    plt.show()


def plot_energy(qubits, ground, first, gap, dt, T):
    """Get the first two eigenvalues and the gap energy
    Args:
        qubits (int): # of total qubits in the instance.
        ground (list): ground state energy during the evolution.
        first (list): first excited state during the evolution.
        gap (list): gap energy during the evolution.
        T (float): Final time for the schedue.
        dt (float): time interval for the evolution.
    Returns:
        {}_qubits_energy.png: energy evolution of the ground and first excited state.
        {}_qubits_gap_energy.png: gap evolution during the adiabatic process.
    """
    fig, ax = plt.subplots()
    times = np.arange(0, T + dt, dt)
    ax.plot(times, ground, label='ground state', color='C0')
    ax.plot(times, first, label='first excited state', color='C1')
    plt.ylabel('energy')
    plt.xlabel('schedule')
    plt.title('Energy during adiabatic evolution')
    ax.legend()
    fig.tight_layout()
    fig.savefig('images/{}_qubits_energy.png'.format(qubits), dpi=300, bbox_inches='tight')
    fig, ax = plt.subplots()
    ax.plot(times, gap, label='gap energy', color='C0')
    plt.ylabel('energy')
    plt.xlabel('schedule')
    plt.title('Energy during adiabatic evolution')
    ax.legend()
    fig.tight_layout()
    fig.savefig('images/{}_qubits_gap.png'.format(qubits), dpi=300, bbox_inches='tight')
    plt.show()
