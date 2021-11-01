# -*- encoding: utf-8 -*-
'''
@File        :run.py
@Time        :2021/09/28 09:04:51
@Author        :charles kiko
@Version        :1.0
@Contact        :charles_kiko@163.com
@Desc        :主程序
'''


import argparse
import os
import sys
import configparser
import pandas as pd
import famCircle
import famCircle.bez as bez
from famCircle.filterWGD import filterWGD
from famCircle.hmmer import hmmer
from famCircle.screen import screen
from famCircle.Ks import Ks
from famCircle.Ks_block import Ks_block
from famCircle.circle import circle
from famCircle.line import line
from famCircle.circle_all import circle_all
from famCircle.circle_family import circle_family
from famCircle.filter_unit import filter_unit

from famCircle.outer import outer
from famCircle.inner import inner

from famCircle.typing import typing
from famCircle.part import part
from famCircle.family_pair import family_pair

from famCircle.tandem import tandem
from famCircle.proximal import proximal
from famCircle.WGD_family import WGD_family
from famCircle.trd import trd
from famCircle.dispersed import dispersed


parser = argparse.ArgumentParser(
    prog = 'famCircle', usage = '%(prog)s [options]', epilog = "", formatter_class = argparse.RawDescriptionHelpFormatter,)
parser.description = '''\
圈图构建
    -------------------------------------- '''
parser.add_argument("-v", "--version", action = 'version', version='0.2.01')

parser.add_argument("-fu", dest = "filter_unit",
                    help = "BLAST文件过滤")
parser.add_argument("-ca", dest = "circle_all",
                    help = "全基因组共线性展示，支持文件格式famCircle/blast/MCScanX/ColinearScan/WGDI")
parser.add_argument("-l", dest = "line",
                    help = "局部共线性展示，支持文件格式famCircle/blast/MCScanX/ColinearScan/WGDI")
parser.add_argument("-c", dest = "circle",
                    help = "全基因组共线性ks展示，支持文件格式famCircle/blast/MCScanX/ColinearScan/WGDI;")
parser.add_argument("-ks", dest = "Ks",
                    help = "全基因组kaks计算，支持文件格式blast/MCScanX/ColinearScan/WGDI;")
parser.add_argument("-kb", dest = "Ks_block",
                    help = "共线性块ks核密度曲线，支持文件格式famCircle/MCScanX/ColinearScan/WGDI;")
parser.add_argument("-hmm", dest = "hmmer",
                    help = "家族成员鉴定;")
parser.add_argument("-fp", dest = "family_pair",
                    help = "比对文件或共线性文件与家族成员相关基因提取，支持文件famCircle/blast/MCScanX/ColinearScan/WGDI;")
parser.add_argument("-cf", dest = "circle_family",
                    help = "家族成员染色体定位;")
parser.add_argument("-s", dest = "screen",
                    help = "染色体内家族成员数量分布统计;")
parser.add_argument("-t", dest = "typing",
                    help = "格式转换;")
parser.add_argument("-o", dest = "outer",
                    help = "家族成员分布及发生时间估计展示;")
parser.add_argument("-i", dest = "inner",
                    help = "家族成员分布及发生时间估计展示;")
parser.add_argument("-p", dest = "part",
                    help = "家族成员分布及发生时间估计展示;")
parser.add_argument("-f", dest = "filterWGD",
                    help = "全基因组共线性文件过滤，支持文件格式ColinearScan/WGDI;")
parser.add_argument("-td", dest = "tandem",
                    help = "串联重复型家族成员筛选及发生时间估计展示;")
parser.add_argument("-pd", dest = "proximal",
                    help = "近端重复家族成员筛选及发生时间估计展示;")
parser.add_argument("-wf", dest = "WGD_family",
                    help = "WGD型家族成员筛选及发生时间估计展示;")
parser.add_argument("-trd", dest = "trd",
                    help = "转座重复家族成员筛选及发生时间估计展示;")
parser.add_argument("-dsd", dest = "dispersed",
                    help = "散在重复家族成员及发生时间估计展示;")


args = parser.parse_args()

def run_filter_unit():
    options = bez.load_conf(args.filter_unit, 'filter_unit')
    filter_unit1 = filter_unit(options)
    filter_unit1.run()

def run_filterWGD():
    options = bez.load_conf(args.filterWGD, 'filterWGD')
    filterWGD1 = filterWGD(options)
    filterWGD1.run()

def run_tandem():
    options = bez.load_conf(args.tandem, 'tandem')
    tandem1 = tandem(options)
    tandem1.run()

def run_proximal():
    options = bez.load_conf(args.proximal, 'proximal')
    proximal1 = proximal(options)
    proximal1.run()

def run_trd():
    options = bez.load_conf(args.trd, 'trd')
    trd1 = trd(options)
    trd1.run()

def run_dispersed():
    options = bez.load_conf(args.dispersed, 'dispersed')
    dispersed1 = dispersed(options)
    dispersed1.run()

def run_hmmer():
    options = bez.load_conf(args.hmmer, 'hmmer')
    hmmer1 = hmmer(options)
    hmmer1.run()

def run_screen():
    options = bez.load_conf(args.screen, 'screen')
    screen1 = screen(options)
    screen1.run()

def run_Ks():
    options = bez.load_conf(args.Ks, 'Ks')
    lookKs0 = Ks(options)
    lookKs0.run()

def run_Ks_block():
    options = bez.load_conf(args.Ks_block, 'Ks_block')
    lookKs0 = Ks_block(options)
    lookKs0.run()

def run_typing():
    options = bez.load_conf(args.typing, 'typing')
    typing1 = typing(options)
    typing1.run()

def run_circle():
    options = bez.load_conf(args.circle, 'circle')
    circle1 = circle(options)
    circle1.run()

def run_line():
    options = bez.load_conf(args.line, 'line')
    circle1 = line(options)
    circle1.run()

def run_circle_all():
    options = bez.load_conf(args.circle_all, 'circle_all')
    circle0 = circle_all(options)
    circle0.run()

def run_WGD_family():
    options = bez.load_conf(args.WGD_family, 'WGD_family')
    WGD_family0 = WGD_family(options)
    WGD_family0.run()

def run_circle_family():
    options = bez.load_conf(args.circle_family, 'circle_family')
    circle0 = circle_family(options)
    circle0.run()

def run_outer():
    options = bez.load_conf(args.outer, 'outer')
    outer1 = outer(options)
    outer1.run()

def run_inner():
    options = bez.load_conf(args.inner, 'inner')
    inner1 = inner(options)
    inner1.run()

def run_part():
    options = bez.load_conf(args.part, 'part')
    inner1 = part(options)
    inner1.run()

def run_family_pair():
    options = bez.load_conf(args.family_pair, 'family_pair')
    family_pair1 = family_pair(options)
    family_pair1.run()

def module_to_run(argument):
    switcher = {
        'filter_unit': run_filter_unit,
        'filterWGD': run_filterWGD,
        'tandem': run_tandem,
        'proximal': run_proximal,
        'trd': run_trd,
        'dispersed': run_dispersed,
        'WGD_family': run_WGD_family,
        'hmmer': run_hmmer,
        'screen': run_screen,
        'Ks': run_Ks,
        'Ks_block': run_Ks_block,
        'typing': run_typing,
        'circle': run_circle,
        'line': run_line,
        'circle_all': run_circle_all,
        'circle_family': run_circle_family,
        'outer': run_outer,
        'inner': run_inner,
        'part': run_part,
        'family_pair': run_family_pair,
    }
    return switcher.get(argument)()

def main():
    path = famCircle.__path__[0]
    options = {
               'filter_unit': 'filter_unit.conf',
               'filterWGD': 'filterWGD.conf',
               'tandem': 'tandem.conf',
               'proximal': 'proximal.conf',
               'trd': 'trd.conf',
               'dispersed': 'dispersed.conf',
               'WGD_family': 'WGD_family.conf',
               'hmmer': 'hmmer.conf',
               'screen': 'screen.conf',
               'Ks': 'Ks.conf',
               'Ks_block': 'Ks_block.conf',
               'typing': 'typing.conf',
               'circle': 'circle.conf',
               'line': 'line.conf',
               'circle_all': 'circle_all.conf',
               'circle_family': 'circle_family.conf',
               'outer': 'outer.conf',
               'inner': 'inner.conf',
               'part': 'part.conf',
               'family_pair': 'family_pair.conf',
               }
    for arg in vars(args):
        value = getattr(args, arg)
        # print(value)
        if value is not None:
            if value in ['?', 'help', 'example']:
                f = open(os.path.join(path, 'example', options[arg]))
                print(f.read())
            elif value == 'e':
                out = '''\
        File example
        [fpchrolen]
        chromosomes number_of_bases
        *   *
        *   *
        *   *
        [fpgff]
        chromosomes gene    start   end
        *   *   *   *
        *   *   *   *
        *   *   *   *
        [fpgenefamilyinf]
        gene1   gene2   Ka  Ks
        *   *   *   *
        *   *   *   *
        *   *   *   *
        [alphagenepairs]
        gene1   gene2
        *   *   *
        *   *   *
        *   *   *

        The file columns are separated by Tab
        -----------------------------------------------------------    '''
                print(out)
            elif not os.path.exists(value):
                print(value+' not exits')
                sys.exit(0)
            else:
                module_to_run(arg)

