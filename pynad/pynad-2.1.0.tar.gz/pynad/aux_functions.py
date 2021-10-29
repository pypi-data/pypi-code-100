#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2020 - Rafael Guerreiro Osorio - Ipea.

pynad - funções auxiliares
"""


import time


PNADCA = 'anual'
PNADCT = 'trimestral'


def csv_nome(nome, pnad):
    """Retorna o nome do arquivo csv a partir do original e tipo de pnad."""
    if pnad == PNADCA:
        stub = '.'.join(nome[:-4].split('_')[1:3])
    if pnad == PNADCT:
        stub = nome[:-4].split('_')
        stub = f'{stub[1][2:]}.{stub[1][1]}'
    nome = ".".join(pnad.split('_'))
    nome = f'microdados.{nome}.{stub}.csv'
    return nome


def elapsed(start):
    """Retorna string com o tempo formatado desde start."""
    end = time.time()
    days = int((end - start) / 86400)
    hours = int((end - start) / 3600)
    mins = int(((end - start) - hours * 3600) / 60)
    segs = int((end - start) - hours * 3600 - mins * 60)
    mils = int(((end - start) - int(end - start)) * 1000)
    if days:
        result = f'{days:.0f} dias'
    elif hours:
        result = f'{hours:.0f}h {mins:2.0f}m {segs:2.0f}s'
    elif mins:
        result = f'{mins:2.0f}m {segs:2.0f}s'
    elif segs:
        result = f'{segs:2.0f}s'
    else:
        result = f'{mils:3.0f}ms'
    return result


def sizestr(size):
    """Retorna string com o tamanho formatado."""
    if size > 10**9:
        sizes = f'{size / 10 ** 9:.1f} GB'
    elif size > 10**6:
        sizes = f'{size / 10 ** 6:.1f} MB'
    elif size > 10**3:
        sizes = f'{size / 10 ** 3:.1f} KB'
    else:
        sizes = f'{size:.1f} Bytes'
    return sizes.replace('.', ',')
