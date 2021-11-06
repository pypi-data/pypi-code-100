import os
import yaml
import re

path_matcher = re.compile(r'\$\{([^}^{]+)\}')


def py_eval(loader, node):
    value = node.value
    return eval(value)


def stats_eval(loader, node):
    seq = loader.construct_sequence(node)
    seq[4] = seq[5] - 3 * seq[8] if seq[7] is None else seq[5] - 3 * seq[7]
    seq[6] = seq[5] + 3 * seq[8] if seq[7] is None else seq[5] + 3 * seq[7]
    return seq


def path_sub(loader, node):
    """ Extract the matched value, expand env variable, and replace the match """
    value = node.value
    value = re.sub(path_matcher, lambda m: os.getenv(m.group(1)), value)
    return value


def path_join(loader, node):
    seq = loader.construct_sequence(node)
    return os.pathsep.join([str(i) for i in seq])


def sep_join(loader, node):
    seq = loader.construct_sequence(node)
    return os.sep.join([str(i) for i in seq])


def space_join(loader, node):
    seq = loader.construct_sequence(node)
    return ' '.join([str(i) for i in seq])


def comma_join(loader, node):
    seq = loader.construct_sequence(node)
    return ', '.join([str(i) for i in seq])


def join(loader, node):
    seq = loader.construct_sequence(node)
    return ''.join([str(i) for i in seq])


yaml.add_constructor('!py', py_eval)
yaml.add_constructor('!stats', stats_eval)

yaml.add_implicit_resolver('!path', path_matcher)
yaml.add_constructor('!path', path_sub)

yaml.add_constructor('!path_join', path_join)
yaml.add_constructor('!sep_join', sep_join)
yaml.add_constructor('!space_join', space_join)
yaml.add_constructor('!comma_join', comma_join)
yaml.add_constructor('!join', join)




