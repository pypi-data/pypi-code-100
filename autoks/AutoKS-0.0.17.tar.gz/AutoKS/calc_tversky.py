#!/usr/bin/env python
# -*- coding: utf-8 -*-

def calc_tversky(
        graph1,
        graph2,
        comparison,
        alpha=0.5,
        detailed=False
):
    """

    goals
    - detailed: if True, print details
    - concept, semantic

    :param detailed: if True, print details
    :param graph1:
    :param graph2:
    :param comparison: ['concept', 'propositional', 'semantic']
    :param alpha:
    :return:
    """

    s = None

    assert comparison in ['concept', 'propositional', 'semantic']

    if comparison == 'concept':
        set1, set2 = concept(graph1, graph2)
        s = tversky(set1, set2, alpha=alpha)
    elif comparison == 'propositional':
        set1, set2 = propositional(graph1, graph2, alpha=alpha, detailed=detailed)
        s = tversky(set1, set2, alpha=alpha)
    if comparison == 'semantic':
        c_set1, c_set2 = concept(graph1, graph2)
        p_set1, p_set2 = propositional(graph1, graph2, alpha=alpha, detailed=detailed)
        s = tversky(p_set1, p_set2, alpha=alpha) / tversky(c_set1, c_set2, alpha=alpha)

    return s


def takefirst(element):
    return element[0]


def concept(graph1, graph2):
    return set(graph1.nodes), set(graph2.nodes)


def propositional(graph1, graph2, alpha, detailed=False):
    list1 = []
    list2 = []

    allnodes = set(list(graph1.nodes) + list(graph2.nodes))
    allnodes = list(allnodes)

    for edge in list(graph1.edges):
        list1.append((allnodes.index(edge[0]), allnodes.index(edge[1])))
    for edge in list(graph2.edges):
        list2.append((allnodes.index(edge[0]), allnodes.index(edge[1])))

    # sort
    list1.sort(key=takefirst)
    list2.sort(key=takefirst)

    set1 = set(list1)
    set2 = set(list2)

    if detailed:

        print(f"\033[4m\033[36m\nCalculating Tversky's similarity in ratio scales\033[0m")
        print(f"\033[36ms = (set1 - set2)/[(set1 - set2) + alpha*(set1 - set2) + beta*(set2 - set1)]\n"
              f"alpha={alpha}, beta={1-alpha}\n")
        print("for more information, please see references below:\n"
              "Tversky, A. (1977). Features of similarity. Psychological Review, 84(4), 327–\n"
              "352. https://doi.org/10.1037/0033-295X.84.4.327\n "
              "Pirnay-Dummer P., Ifenthaler D. (2010) Automated Knowledge Visualization and \n"
              "Assessment. In: Ifenthaler D., Pirnay-Dummer P., Seel N. (eds) Computer-Based \n"
              "Diagnostics and Systematic Analysis of Knowledge. Springer, Boston, MA. \n"
              "https://doi.org/10.1007/978-1-4419-5662-0_6\n"
              )

        # set1 & set2
        intersection = content_in_set(set1 & set2, allnodes)
        print('set1 & set2:', intersection)
        print('value of set1 & set2:', len(intersection))

        # set1 - set2
        difference1 = content_in_set(set1 - set2, allnodes)
        print('set1 - set2:', difference1)
        print('value of set1 - set2:', len(difference1))
        difference2 = content_in_set(set2 - set1, allnodes)
        print('set2 - set1:', difference2)
        print('value of set2 - set1:', len(difference2))

        print(f"similarity = {len(intersection)}/"
              f"({len(intersection)} + {alpha}*{len(difference1)} + {1-alpha}*{len(difference2)})"
              f"={len(intersection)/(len(intersection)+alpha*len(difference1)+(1-alpha)*len(difference2))}\033[0m")

    return set1, set2


def content_in_set(my_set, allnodes):
    my_set = list(my_set)
    content = []
    for i in range(0, len(my_set)):
        content.append([allnodes[my_set[i][0]], allnodes[my_set[i][1]]])
    return content


def tversky(set1, set2, alpha=0.5):

    if set1 != set2:
        beta = 1 - alpha
        s = len(set1 & set2) / (len(set1 & set2) +
                                alpha * len(set1 - set2) +
                                beta * len(set2 - set1))
    else:
        s = 1

    s = float('%.4f' % s)

    return s
