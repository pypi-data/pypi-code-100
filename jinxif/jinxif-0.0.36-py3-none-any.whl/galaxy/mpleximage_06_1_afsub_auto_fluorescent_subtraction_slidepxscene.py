#####
# title: mpleximage_06_1_afsub_auto_fluorescent_subtraction_slidepxscene.py
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
####


# library
import argparse
from jinxif import afsub
import json
import os

# function
def afsub_slidepxscene(
        es_exclude_color,
        es_exclude_marker,
        b_8bit,
    ):
    '''
    input: 
      registered image tiff files unter the input directory.

    output:
      afsubtracted tiff images in the output directory.

    description:
      do auto fluorescent subtraction on registered images. 
    '''
    # load ddd_etc exposure time correction
    ddd_etc =  json.load(open('ddd_etc.json'))
    print('ddd_etc:', ddd_etc)

    # load ddd_crop for slide_mscene slide_pxscene mapping
    ddd_crop =  json.load(open('ddd_crop.json'))
    print('ddd_crop:', ddd_crop)

    # load ds_early.json
    ds_early = json.load(open('ds_early.json'))
    print('ds_early:', ds_early)

    # load ds_late.json
    ds_late = json.load(open('ds_late.json'))
    print('ds_late:', ds_late)

    # function call
    afsub._make_afsubtract_images(
        ddd_crop = ddd_crop,  # to add exposure time
        ddd_etc = ddd_etc,  # to add exposure time
        ds_early = ds_early,
        ds_late = ds_late,
        es_exclude_color = es_exclude_color,
        es_exclude_marker = es_exclude_marker,
        b_8bit = b_8bit,
        # file system
        s_metadir = 'metaimages/',  # to add exposure time
        s_regdir_slidepxscene = 'tiff_registered/',  # input files
        s_afsubdir_slidepxscene = 'tiff_afsub/',  # output files
    )


# run from the command line
if __name__ == '__main__':

    # specify command line argument
    parser = argparse.ArgumentParser(description='run jinxif.galaxy.afsub_slidepxscene.')
    parser.add_argument(
        '--xcolor',
        help='',
        type=str,
        nargs='*', # bue: will turn the output into a list of strings.
    )
    parser.add_argument(
        '--xmarker',
        help='',
        type=str,
        nargs='*', # bue: will turn the output into a list of strings.
    )
    parser.add_argument(
       '--bit8',
       help='',
       type=str,
       default='false',
       #nargs=1, # bue: will turn the output into a list of strings.
    )
    args = parser.parse_args()
    print('es_exclude_color:', args.xcolor)
    print('es_exclude_marker:', args.xmarker)
    print('s_bit8:', args.bit8)

    # run code
    b_8bit = False
    if args.bit8 in {'true', 'True'}:
        b_8bit = True
    afsub_slidepxscene(
        es_exclude_color = args.xcolor,  # {'c1','c5'},
        es_exclude_marker = args.xmarker,  # {},
        b_8bit = b_8bit,  # False,
    )

