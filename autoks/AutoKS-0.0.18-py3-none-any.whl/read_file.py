# !/usr/bin/env python
# -*- coding: utf-8 -*-

def read_file(filepath,
              encoding='utf-8'):
    """
    read file into a list
    :param filepath:
    :param encoding:
    :return:
    """
    content = []
    f = open(filepath, "r", encoding=encoding)
    for line in f.readlines():
        line = line.strip('\n')  # remove "\n" in "node1 \t node2 \n"
        if '\t' in line:
            content.append(line.split('\t'))  # split to each element in a list by "\t"
        else:
            line = line.split(' ')  # split to each element in a list by " " (i.e., space)
            if '' in line:
                line.remove('')  # delete the element that have "" value
            content.append(line)
    f.close()
    return content
