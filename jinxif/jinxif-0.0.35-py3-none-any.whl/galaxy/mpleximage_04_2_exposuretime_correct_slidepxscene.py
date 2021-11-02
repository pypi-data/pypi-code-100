#####
# title: mpleximage_04_2_exposuretime_correct_slidepxscene.py
#
# language: Python3
# date: 2021-08-19
# license: GPLv>=3
# autor: bue
#
# description:
#   galaxy tool wrapper for jinxif pipeline element
#   + https://github.com/galaxyproject/galaxy
#   + https://gitlab.com/bue/jinxif
#####


# library
#import argparse
from jinxif import config
from jinxif import regist
import json
import os
import re
import shutil


# function
def exposuretime_correct_slidepxscene():
    '''
    input:
        tiff files under the tiff_registered/ directory.
        json file ddd_etc.json

    output:
        tiff files under the tiff_registered/ directory.

    description:
        copy registerd tiff files and exposure time correct them, if specified in ddd_etc.json.
    '''

    # get exposure time correct slidepz scenes
    ddd_etc = json.load(open('tiff_registered/ddd_etc.json'))
    es_slidepxscene_etc = set(ddd_etc.keys())

    # get registerd slidepxscenes
    for s_file in sorted(os.listdir('tiff_registered/')):
        print(f'check: {s_file} ...')
        o_match = re.search(config.d_nconv['s_regex_tiff_reg'], s_file)
        if not (o_match is None):

            print(f'found registered image file: {s_file}')
            s_slide = o_match[config.d_nconv['di_regex_tiff_reg']['slide']]
            s_scene = o_match[config.d_nconv['di_regex_tiff_reg']['scene']]
            s_slidepxscene_reg  = s_slide + '_' + s_scene

            # get markers etc
            try: 
                es_marker_etc = set(ddd_etc[s_slidepxscene_reg].keys())
            except KeyError:
                es_marker_etc = {}

            # get marker reg
            ls_marker = o_match[config.d_nconv['di_regex_tiff_reg']['markers']].split(config.d_nconv['s_sep_marker_jinxif'])
            ls_marker.insert(0, config.d_nconv['s_marker_dapi'])
            ls_color = config.d_nconv['ls_color_order_jinxif']
            s_color = o_match[config.d_nconv['di_regex_tiff_reg']['color']]
            s_marker_reg = ls_marker[ls_color.index(s_color)]

            # manipulate
            if (s_slidepxscene_reg in es_slidepxscene_etc) and (s_marker_reg in es_marker_etc):
                # exposure time correct
                print(f'exposure time correct: {s_file}')
                dd_marker_etc = ddd_etc[s_slidepxscene_reg]
                regist._make_exposure_time_correct(
                    s_slidepxscene = s_slidepxscene_reg,
                    dd_marker_etc = dd_marker_etc,
                    s_imagetype_original = 'ORG',
                    # file system
                    s_regpath = 'tiff_registered/',
                )
            else:
                # nop
                print(f'skip: {s_file}')


# run from the command line
if __name__ == '__main__':

    # function call
    exposuretime_correct_slidepxscene()

