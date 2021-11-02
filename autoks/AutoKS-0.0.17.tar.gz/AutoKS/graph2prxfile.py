#!/usr/bin/env python
# -*- coding: utf-8 -*-

import networkx as nx


def graph2prxfile(G, filetype, filename, keyterm_list=None, encoding='UTF-8'):
    """
    save each edge in a Graph into a prx file
    :param G:
    :param filetype: 'pair' or 'array'
    :param filename:
    :param encoding:
    :return:
    """

    try:

        output = None

        if filetype == 'array':
            # convert Graph into proximity array
            matrix_str = str(nx.to_numpy_array(G, dtype=int, nodelist=keyterm_list))  # matrix_str = '[[0 1 0 1 0]\n [1 0 1 0 1]\n ...'
            repl = {'[': '',
                    ']': '',
                    '\n ': '\n',
                    ' ': '\t'}
            for i in repl:
                matrix_str = matrix_str.replace(i, repl[i])  # matrix_str = '0 1 0 1 0\n1 0 1 0 1\n...'
            # print(matrix_str)

            # output content
            nodes_num = None
            if keyterm_list:
                nodes_num = len(keyterm_list)
            else:
                nodes_num = len(G.nodes)
            output = f"""DATA\nsimilarities\n{nodes_num} item\n1 decimals\n0.1 min\n1 max\nmatrix:\n{matrix_str}"""

        if filetype == 'pair':

            output = ''
            for pair in G.edges:
                output += f'{pair[0]}\t{pair[1]}\n'

            output = output[:-2]  # remove the last '\n'

        # write file
        with open(filename + '.prx', 'w', encoding=encoding) as f:
            f.write(output)

    except IOError:
        print('ERROR!')
    else:
        print(f'Prx file is saved! File name is "{filename}.prx".')
