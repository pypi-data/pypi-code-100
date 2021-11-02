#!/usr/bin/env python3

import importlib.util
import pathlib

import importlib_metadata

def get_distribution(file_name):
    result = None
    for distribution in importlib_metadata.distributions():
        try:
            relative = (
                pathlib.Path(file_name)
                .relative_to(distribution.locate_file(''))
            )
        except ValueError:
            pass
        else:
            if distribution.files and relative in distribution.files:
                result = distribution
                break
    return result

def alpha():
    file_name = importlib.util.find_spec('serial').origin
    distribution = get_distribution(file_name)
    print("alpha", distribution.metadata['Name'])

def bravo():
    import serial
    file_name = serial.__file__
    distribution = get_distribution(file_name)
    print("bravo", distribution.metadata['Name'])

if __name__ == '__main__':
    alpha()
    bravo()

