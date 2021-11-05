# !/usr/bin/env python
# -*- coding: utf-8 -*-

import networkx as nx
from os.path import basename
from .pathfinder_network import *
from .read_file import *


def cmap2graph(
        file,
        data_type,
        keyterms=None,
        encoding='utf-8',
        read_from_file=True,
        read_from=0,
        pfnet=False,
        sim_max=None,
        sim_min=None,
        r=np.inf):
    r"""

    This implementation is based on Kanevsky's algorithm [1]_ for finding all
    -------------------------------



    format: ['pairs', 'array'], noted that matrix in ['similarity', 'dissimilarity', 'proximity']
    read_form: 7 or (7,10) or [7,10], noted that 10 is the last line

    Done:
    - format: 1) propositions, 2) matrix, included similarity/dissimilarity
    - set the begin line

    Goals:
    - directed/undirected type
    - label/without label type

    """

    try:
        assert data_type in ['pair', 'array']
    except:
        print('\033[0;31m\nERROR: the value of "data_type" is unrecognized, '
              'it must be either "pair" or "array"!\033[0m')
        exit(1)

    G = nx.Graph()

    if read_from_file:
        G.name = basename(file.split('.')[0])

        # Step 1: read file, each line in the file, add each line into the list
        content = read_file(file, encoding=encoding)
    else:
        content = list(file)

    # Step 2: find data by index (i.e., the parameter 'read_from'), skip the unwanted content
    if type(read_from) == int:
        content = content[read_from:]
    elif type(read_from) in [tuple, list]:
        content = content[read_from[0]:read_from[1]]
    if data_type == 'array':
        # Step 3-1: convert the triangle matrix to a n*n matrix (if necessary)
        # this means a triangle matrix
        # add first row, this is m[0, 0]
        # add elements in each row until the number of elements equal to n
        if len(content[0]) != len(content[-1]):
            content.insert(0, ['0'])
            for i in range(0, len(content)):
                while len(content[i]) != len(content):
                    content[i].append('')
            # Step 3-2: add value
            # for each element m[i, j]
            # for each element in the diagonal line
            # for each element in the upper part of the triangle
            for i in range(0, len(content)):
                for j in range(0, len(content)):
                    if i == j:
                        content[i][j] = '0'
                    elif i < j:
                        content[i][j] = content[j][i]
        # Step 3-3: convert each value from string to int
        array = np.zeros([len(content), len(content)])
        for i in range(0, len(content)):
            for j in range(0, len(content)):
                array[i, j] = int(content[i][j])

        # Step 4: calculate PFNet (if necessary)
        if pfnet:
            if sim_max is not None and sim_min is not None:  # similarity --> distances (if necessary)
                array = sim_max - array + sim_min
                # the value that out of range would be set as inf
                array = np.where((array > sim_min) & (array < sim_max), array, np.inf)

            array = floyd(array, r=r)

        # Step 5: convert it to a graph
        start, end = np.where(np.tril(array) == True)
        pairs = []
        for i in range(0, len(start)):
            pairs.append([keyterms[start[i]], keyterms[end[i]]])
        G.add_edges_from(pairs)
    elif data_type == 'pair':
        for pair in content:
            G.add_edge(pair[0], pair[1])

    return G
