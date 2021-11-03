"""Paquete principal del framework que contiene los modulos para obtener soluciones a problemas TSP"""
import argparse
import math
import os
import sys
import time
from enum import Enum
from decimal import Decimal

from TSPF import utilities
from TSPF.utilities import bcolors, Trajectory
from TSPF.TSPlibReader import TSPlibReader
from TSPF.AlgorithmsOptions import AlgorithmsOptions, InitialSolution, CoolingType, MHType, SelectionStrategy, SelectionType, CrossoverType, TSPMove
from TSPF.Tsp import Tsp
from TSPF.Tour import Tour
from TSPF import plot