#####
# title: mpleximage_09_1_feature_extraction_slidepxscene.py
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
from jinxif import config
from jinxif import feat
import os
import re
import shutil
import sys

# function
def extract_features_slidepxscene(
        s_input,
        s_thresh_marker,
        i_exp,
        i_mem,
        i_shrink,
    ):
    '''
    input: 

    output:

    description:
    '''
    # get slide_pxscene
    es_slidepxscene = set()
    for s_filename  in os.listdir('tiff_registered/'):
        print(f'checking: tiff_registered/{s_filename} ...')
        o_match = re.search(config.d_nconv['s_regex_tiff_reg'], s_filename)
        if not (o_match is None):
            s_slide = o_match[config.d_nconv['di_regex_tiff_reg']['slide']]  # bue: given as function input!
            s_pxscene = o_match[config.d_nconv['di_regex_tiff_reg']['scene']]
            s_slidepxscene = f'{s_slide}_{s_pxscene}'
            es_slidepxscene.add(s_slidepxscene)
    if (len(es_slidepxscene) != 1):
        sys.exit(f'Error: in tiff_registered/ more or less then one slide_pxscene found {sorted(es_slidepxscene)}.')
    s_slidepxscene = es_slidepxscene.pop()

    # get tiff_registered/ in shape
    shutil.move('tiff_registered', s_slidepxscene)
    os.makedirs('tiff_registered', exist_ok=True)
    shutil.move(s_slidepxscene, 'tiff_registered/')

    # remove possible existing temp output file
    s_ofile_tmp = config.d_nconv['s_format_csv_raw_centroid_shape_meanintenisty'].format(s_slide, s_input) + '.part'
    try:
        os.remove(f'tiffpng_segmentation/{s_ofile_tmp}')
    except FileNotFoundError:
        pass

    # subfunction call
    feat._make_extract_features(
        s_thresh_marker = s_thresh_marker,
        i_exp = i_exp,
        i_mem = i_mem,
        i_shrink = i_shrink,
        # specify input and output directory
        s_input = s_input,
        s_afsubdir = 'tiff_registered/',
        s_format_afsubdir = config.d_nconv['s_format_afsubdir'],
        s_segpath = 'tiffpng_segmentation/',
        s_feraw_file_tmp = s_ofile_tmp,
    )

    # write slide output to file
    s_ofile = config.d_nconv['s_format_csv_raw_centroid_shape_meanintenisty'].format(s_slidepxscene, s_input)
    shutil.move(f'tiffpng_segmentation/{s_ofile_tmp}', f'csv_segmentation/{s_ofile}')
    print(f'rename: tiffpng_segmentation/{s_ofile_tmp} to csv_segmentation/{s_ofile}')
    #break



# run from the command line
if __name__ == '__main__':

    # specify command line argument
    parser = argparse.ArgumentParser(description='run jinxif.galaxy.extract_features_slidepxscene.')
    parser.add_argument(
        '--imagetype',
        help='',
        type=str,
        #nargs='*', # bue: will turn the output into a list of strings.
    )
    parser.add_argument(
        '--cmarker',
        help='',
        type=str,
        #nargs='*', # bue: will turn the output into a list of strings.
    )
    parser.add_argument(
        '--exp',
        help='',
        type=int,
        #nargs='*', # bue: will turn the output into a list of strings.
    )
    parser.add_argument(
        '--mem',
        help='',
        type=int,
        #nargs='*', # bue: will turn the output into a list of strings.
    )
    parser.add_argument(
        '--shrink',
        help='',
        type=int,
        #nargs='*', # bue: will turn the output into a list of strings.
    )
    args = parser.parse_args()
    print('s_input:', args.imagetype, type(args.imagetype))
    print('s_thresh_marker:', args.cmarker, type(args.cmarker))
    print('i_exp:', args.exp, type(args.exp))
    print('i_mem:', args.mem, type(args.mem))
    print('i_shrink:', args.shrink, type(args.shrink))

    # run code
    if (args.cmarker in {'None', 'none'}):
        s_thresh_marker = None
    else:
        s_thresh_marker = args.cmarker
    extract_features_slidepxscene(
        s_input = args.imagetype,
        s_thresh_marker = s_thresh_marker,
        i_exp = args.exp,  # 5,
        i_mem = args.mem,  # 2,
        i_shrink = args.shrink,  # 1,
    )

