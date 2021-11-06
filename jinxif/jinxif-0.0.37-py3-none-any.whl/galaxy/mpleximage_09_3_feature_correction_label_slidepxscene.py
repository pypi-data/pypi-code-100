#####
# title: mpleximage_09_3_feature_correction_label_slidepxscene.py
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
import json
import os
import shutil
import sys

# function
def feature_correction_label_slidepxscene(
        i_thresh_manual,
        s_thresh_marker,
        i_exp ,
    ):
    '''
    input:

    output:

    description:
    '''
    # get feature raw csv fileaname
    ls_file = os.listdir('csv_segmentation/')
    if (len(ls_file) != 1):
        sys.exit('Error: more then one or no features raw csv file found {ls_file}.')
    s_csv_rawfeature = ls_file[0]
    s_manipu = s_csv_rawfeature

    # extract s_slidepxscene and s_input from feature raw csv fileaname
    #'s_format_csv_raw_centroid_shape_meanintenisty': 'features_{}_raw_MeanIntensity_Shape_Centroid_{}.csv',  # s_slide, s_input
    ls_erase = config.d_nconv['s_format_csv_raw_centroid_shape_meanintenisty'].split('{}')
    for s_erase in ls_erase:
        s_manipu = s_manipu.replace(s_erase,'/')
    ls_manipu = s_manipu.split('/')
    ls_slidepxscene_input = []
    for s_manipu in ls_manipu:
        if (s_manipu != ''):
            ls_slidepxscene_input.append(s_manipu)
    s_slidepxscene = ls_slidepxscene_input[0]
    s_input = ls_slidepxscene_input[1]

    # move fearure csv into segmentation directory
    shutil.move(f'csv_segmentation/{s_csv_rawfeature}', 'segmentation/')

    # manipulate segementation directory
    s_path_seg = config.d_nconv['s_format_segdir_cellpose'].format('segmentation/', s_slidepxscene)  #'{}{}_CellposeSegmentation/'  # s_segdir, s_slide_pxscene
    s_subdir = s_path_seg.replace('segmentation/','')
    shutil.move('segmentation/', s_subdir)
    os.makedirs('segmentation/', exist_ok=False)
    shutil.move(s_subdir, 'segmentation/')

    # load mean intensity segmentation feature datatframe
    df_mi = feat.load_cellpose_features_df(
        es_slide = {s_slidepxscene},
        s_afsubdir = f'{s_input}/',
        s_segdir = 'segmentation/',
        s_format_segdir_cellpose = config.d_nconv['s_format_segdir_cellpose'],
    )

    # get cells without cytoplasm
    feat._thresh_cytoplasm(
        df_mi = df_mi,
        i_thresh_manual = i_thresh_manual,
        s_thresh_marker = s_thresh_marker,
    )

    # each slide_pxscene
    ddls_touch = {}

    # function call
    feat._make_feature_correct_labels(
        df_mi = df_mi,
        ddls_touch = ddls_touch,
        s_thresh_marker = s_thresh_marker,
        i_exp = i_exp,
        s_ipath = s_path_seg,
        s_opath = 'output/',
    )

    # save ddls_touch as json file
    with open('output/' + config.d_nconv['s_format_json_celltouch_segmentation'].format(s_slidepxscene), 'w') as f:
        json.dump(ddls_touch[s_slidepxscene], f)
    # break


# run from the command line
if __name__ == '__main__':

    # specify command line argument
    parser = argparse.ArgumentParser(description='run jinxif.galaxy.feature_correction_label_slidepxscene.')
    parser.add_argument(
        '--cytopmtheshold',
        help='',
        type=int,
        #nargs='*', # bue: will turn the output into a list of strings.
    )
    parser.add_argument(
        '--cytopm',
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
    args = parser.parse_args()
    print('i_thresh_manual:', args.cytopmtheshold, type(args.cytopmtheshold))
    print('s_thresh_marker:', args.cytopm, type(args.cytopm))
    print('i_exp:', args.exp, type(args.exp))

    # run code
    feature_correction_label_slidepxscene(
        i_thresh_manual = args.cytopmtheshold,
        s_thresh_marker = args.cytopm,
        i_exp = args.exp,
    )
