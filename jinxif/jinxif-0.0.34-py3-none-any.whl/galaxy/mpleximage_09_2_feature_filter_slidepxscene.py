#####
# title: mpleximage_09_2_feature_filter_slidepxscene.py
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
from jinxif import basic
from jinxif import config
from jinxif import feat
from jinxif import thresh
import json
import os
import pandas as pd
import re
import shutil
import sys

# function
def features_filter_slidepxscene(
        es_dapipartition_filter,
        i_thresh_manual,
        s_thresh_marker,
        i_exp,
        i_mem,
        i_shrink,
        es_marker_needed,
        es_custom_markerpartition,
        es_shrink_marker,
        b_filter_na,
    ):
    '''
    input: 

    output:

    description:
    '''
    # get feature raw csv fileaname
    ls_file = os.listdir('segmentation/')
    if (len(ls_file) != 1):
        sys.exit('Error: more then one or no features raw csv file found {ls_file}.')
    s_manipu = ls_file[0]

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

    # manipulate registered dir 
    shutil.move('registered/', s_input)
    
    # manipulate segementation dir
    s_path_seg = config.d_nconv['s_format_segdir_cellpose'].format('segmentation/', s_slidepxscene)  #'{}{}_CellposeSegmentation/'  # s_segdir, s_slide_pxscene
    s_subdir = s_path_seg.replace('segmentation/','')
    shutil.move('segmentation/', s_subdir)
    os.makedirs('segmentation/', exist_ok=False)
    shutil.move(s_subdir, 'segmentation/')

    # handle input
    es_marker_needed = es_marker_needed.union(es_dapipartition_filter)
    es_cytoplasm_marker = config.es_cytoplasmmarker_standard.copy()
    if not (s_thresh_marker is None):
        es_marker_needed.add(s_thresh_marker)
        es_cytoplasm_marker.add(s_thresh_marker)

    # load shape and centroid json
    ds_feature_shape = json.load(open('input/ds_feature_shape.json'))
    ds_feature_centroid = json.load(open('input/ds_feature_centroid.json'))

    # load threshold and round parameter file
    df_img_thresh = thresh.load_thresh_df(
        es_slide = {s_slidepxscene},
        i_thresh_manual = i_thresh_manual,
        s_thresh_marker = s_thresh_marker,
        s_afsubdir = f'{s_input}/',
    )

    # load mean intensity segmentation feature datatframe
    df_mi = feat.load_cellpose_features_df(
        es_slide = {s_slidepxscene},
        s_afsubdir = f'{s_input}/',
        s_segdir = 'segmentation/',
        s_format_segdir_cellpose = config.d_nconv['s_format_segdir_cellpose'],
    )

    # generate features_{s_slide}_CentroidXY.csv files
    ls_coor = ['slide','slide_scene','cellid']  # feat.load_cellpose_features_df takes care of that
    ls_standard = sorted(ds_feature_centroid.values())
    df_xy = df_mi.copy()
    df_xy.rename(ds_feature_centroid, axis=1, inplace=True)
    df_xy = df_xy.loc[:, ls_coor+ls_standard]
    print(f'filter_cellpose_xy {s_slidepxscene}: for quality control make sure centroids dont have too many NAs: {round(df_xy.isna().sum().sum() / (df_xy.shape[0] * df_xy.shape[1]), 3)}[fraction]')
    df_xy = df_xy.dropna(axis=0, how='any')
    # output
    df_xy.to_csv('output/' + config.d_nconv['s_format_csv_centroidxy'].format(s_slidepxscene))

    # detect cytoplasm negagative cells
    if not (s_thresh_marker is None):
        #_fill_cellpose_nas(
        feat._thresh_cytoplasm(
            df_mi = df_mi,
            i_thresh_manual = i_thresh_manual,
            s_thresh_marker = s_thresh_marker,
        )

    # patch bleed through by shrunk marker.
    #_shrunk_seg_regions(
    feat._patch_bleedthrough(
        df_mi = df_mi,
        es_shrink_marker = es_shrink_marker, # list of shrunken marker that should replace perinuc{i_exp} or cytoplasm.
        i_exp = i_exp,
        i_shrink = i_shrink,
    )

    # patch cells without cytoplasm
    if not (s_thresh_marker is None):
        #_fill_cellpose_nas(
        feat._patch_nucleus_without_cytoplasm(
            df_mi = df_mi,
            i_exp = i_exp,
            s_thresh_marker = s_thresh_marker,
        )

    # patch nuc and cell membran marker with weak signal
    #_fill_bright_nas(
    feat._patch_weak_membrane_marker(
        df_mi = df_mi,
        s_thresh_marker = s_thresh_marker,
        i_exp = i_exp,
        i_mem = i_mem,
    ) 

    # filter for nuclei, perinuc5, nucmem2, cellmem2 accoring to config.es_markerpartition_standard
    # and marker specified by es_cyto_marker, es_custom_markerpartition, and es_shape.
    #filter_loc_cellpose(
    df_mi = feat._filter_cellpartition_and_shape(
        df_mi = df_mi,
        s_thresh_marker = s_thresh_marker,
        es_cytoplasm_marker = es_cytoplasm_marker,  # have not to specify cell partition
        es_custom_markerpartition = es_custom_markerpartition, # have to specify cell partition
        i_exp = i_exp,
        i_mem = i_mem,
        ds_shape = ds_feature_shape,
        b_filter_na = b_filter_na,
    )

    # drop last round
    r_last_round, es_marker_todrop = basic.find_last_round(
        df_img = df_img_thresh,  # this is actually the tresholdli file, could be an other one.
        es_marker_needed = es_marker_needed, # e.g. ('DAPI2_nuc','DAPI11_nuc','Ecad')  #
    )
    feat.drop_marker(
        df_mi, # mean intensity values
        es_marker_todrop = es_marker_todrop,
    )

    # apply threshold
    # jenny 2021-07-14: this li auto-treshholding works only for dapi and is used for filtering dapi positive cells!
    #auto_threshold(
    dfb_thresh = thresh.apply_thresh(
        df_mi = df_mi,  # from load_cellpose_df
        df_img_thresh = df_img_thresh,  # from load_thresh_df
    )

    # filter dapi
    # generate qc line plot for tissue loss (defiend by dapi)
    # filter by cell positive for DAPI autotresholding, in round specified in es_dapipartition_filter
    #filter_dapi_cellpose(
    df_mi = feat._filter_dapi_positive(
        df_mi = df_mi,
        dfb_thresh = dfb_thresh,
        es_dapipartition_filter = es_dapipartition_filter,
        s_qcdir = 'output/',  # hack
        s_segdir = '/', # hack
        #s_format_segdir_cellpose = s_format_segdir_cellpose,
    )

    # bue 20210624: if dapi2 should be renamed to dapi and all other dapi should be droped, this have to be here.

    # write df_mi to file at s_format_segdir
    s_filter_dapi = '_'.join([s_filter.split('_')[0] for s_filter in sorted(es_dapipartition_filter)])
    s_ofile = config.d_nconv['s_format_csv_patched_shape_meanintenisty'].format(s_slidepxscene, s_filter_dapi, df_mi.index.name)
    print(f'write file: {s_ofile}')
    df_mi.to_csv('output/' + s_ofile)
    #df_mi.to_csv(s_path_seg + s_ofile)

    # generate qc plot for tissue loss (dapi) and cancer cells (ecad)
    # get all dapi_nuclei columns
    es_dapinuclei = set(dfb_thresh.columns[dfb_thresh.columns.str.contains(config.d_nconv['s_marker_dapi']) & dfb_thresh.columns.str.endswith('_nuclei')].unique())
    # order dapi
    se_dapinuclei = pd.Series(list(es_dapinuclei), name='dapiround')
    se_dapinuclei.index = [float(re.sub(r'[^\d.]','', s_dapiround.replace(config.d_nconv['s_quenching_jinxif'],'.5'))) for s_dapiround in se_dapinuclei]
    se_dapinuclei.sort_index(inplace=True)
    ls_dapinuclei = list(se_dapinuclei.values)
    ls_marker_partition = ls_dapinuclei
    # add cytoplasm marker
    if not (s_thresh_marker is None):
        ls_marker_partition.append(f'{s_thresh_marker}_cytoplasm')
    # plot
    thresh.markerpositive_scatterplot(
        s_slidepxscene = s_slidepxscene,
        df_img_thresh = df_img_thresh,
        dfb_thresh = dfb_thresh,
        df_xy = df_xy,  # generated above
        ls_marker_partition = ls_marker_partition,
        # file system
        s_opath = 'output/',
    )

    # break


# run from the command line
if __name__ == '__main__':

    # specify command line argument
    parser = argparse.ArgumentParser(description='run jinxif.galaxy.features_filter_slidepxscene.')
    parser.add_argument(
        '--dapifilter',
        help='',
        type=str,
        nargs='+', # bue: will turn the output into a list of strings.
    )
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
    parser.add_argument(
        '--mneeded',
        help='',
        type=str,
        nargs='*', # bue: will turn the output into a list of strings.
    )
    parser.add_argument(
        '--custommp',
        help='',
        type=str,
        nargs='*', # bue: will turn the output into a list of strings.
    )
    parser.add_argument(
        '--shrinkm',
        help='',
        type=str,
        nargs='*', # bue: will turn the output into a list of strings.
    )
    parser.add_argument(
       '--filterna',
       help='',
       type=str,
       default='false',
       #nargs=1, # bue: will turn the output into a list of strings.
    )
    args = parser.parse_args()
    print('es_dapipartition_filter:', args.dapifilter, type(args.dapifilter))
    print('i_thresh_manual:', args.cytopmtheshold, type(args.cytopmtheshold))
    print('s_thresh_marker:', args.cytopm, type(args.cytopm))
    print('i_exp:', args.exp, type(args.exp))
    print('i_mem:', args.mem, type(args.mem))
    print('i_shrink:', args.shrink, type(args.shrink))
    print('es_marker_needed:', args.mneeded, type(args.mneeded))
    print('es_custom_markerpartition:', args.custommp, type(args.custommp))
    print('es_shrink_marker:', args.shrinkm, type(args.shrinkm))
    print('s_filter_na:', args.filterna, type(args.filterna))

    # run code
    if (args.cytopm in {'None', 'none'}):
        s_thresh_marker = None
    else:
        s_thresh_marker = args.cytopm
    if (args.filterna in {'True','true'}):
        b_filter_na = True
    else:
        b_filter_na = False
    features_filter_slidepxscene(
        es_dapipartition_filter = args.dapifilter,
        i_thresh_manual = args.cytopmtheshold,
        s_thresh_marker = s_thresh_marker,
        i_exp = args.exp,
        i_mem = args.mem,
        i_shrink = args.shrink,
        es_marker_needed = set(args.mneeded),
        es_custom_markerpartition = set(args.custommp),
        es_shrink_marker = set(args.shrinkm),
        b_filter_na = b_filter_na,
    )
