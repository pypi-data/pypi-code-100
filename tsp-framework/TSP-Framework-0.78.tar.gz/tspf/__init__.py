"""Paquete principal del framework que contiene los modulos para obtener soluciones a problemas TSP"""
import argparse
import math
import os
import sys
import time
from enum import Enum
from decimal import Decimal

from tspf import utilities
from tspf.utilities import bcolors, Trajectory
from tspf.TSPlibReader import TSPlibReader
from tspf.AlgorithmsOptions import AlgorithmsOptions, InitialSolution, CoolingType, MHType, SelectionStrategy, SelectionType, CrossoverType, TSPMove
from tspf.Tsp import Tsp
from tspf.Tour import Tour
from tspf import plot