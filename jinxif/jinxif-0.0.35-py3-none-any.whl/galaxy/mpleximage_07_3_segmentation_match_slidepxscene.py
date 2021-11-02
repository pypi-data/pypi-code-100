#####
# title: mpleximage_07_3_segmentation_match_slidepxscene.py
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
from jinxif import segment
from jinxif import config
import os
import re
import sys

# function
def segment_match_slidepxscene(
        s_type_data,
    ):
    '''
    input: 
      nucleus and cell segementaion basin file unter the input directory.

    output:
      nucleus label matched cell segmentaion basin file.

    description:
      match cell segemenation label to nucleus segemnation label. 
    '''
    # get slide_pxscene
    es_slidepxscene = set()
    for s_filename in os.listdir('tiff_segmentation/'):
        print(f'checking: tiff_segmentation/{s_filename} ...')
        o_match = re.search(config.d_nconv['s_regex_tiff_celllabel_nuc'], s_filename)
        if not (o_match is None):
            s_slide = o_match[config.d_nconv['di_regex_tiff_celllabel_nuc']['s_slide']]  # bue: given as function input!
            s_pxscene = o_match[config.d_nconv['di_regex_tiff_celllabel_nuc']['s_pxscene']]
            s_slidepxscene = f'{s_slide}_{s_pxscene}'
            es_slidepxscene.add(s_slidepxscene)
    if (len(es_slidepxscene) != 1):
        sys.exit(f'Error: in tiff_segmentation/ more or less then one slide_pxscene found {sorted(es_slidepxscene)}.')
    s_slidepxscene = es_slidepxscene.pop()

    # function call
    segment._make_match_nuccell_labels(
        s_slide_pxscene = s_slidepxscene,
        s_type_data = s_type_data,
        # file system
        s_segpath = 'tiff_segmentation/',
    )


# run from the command line
if __name__ == '__main__':

    # specify command line argument
    parser = argparse.ArgumentParser(description='run jinxif.galaxy.segment_match_slidepxscene.')
    parser.add_argument(
        '--datatype',
        help='',
        type=str,
        #nargs='*', # bue: will turn the output into a list of strings.
    )
    args = parser.parse_args()
    print('s_type_data:', args.datatype, type(args.datatype))

    # run code
    segment_match_slidepxscene(
        s_type_data = args.datatype,
    )

