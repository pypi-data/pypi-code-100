#####
# title: mpleximage_07_2_segmentation_cell_slidepxscene.py
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
from jinxif import segment
import sys

# function
def segment_cell_slidepxscene(
        i_cell_diam,
        s_dapi_round,
        es_seg_marker,
        es_rare_marker,
        b_gpu,
    ):
    '''
    input: 
      registered image tiff files unter the input directory.

    output:
      cell segmentaion basin label files.

    description:
      do cellpose cytoplasm segmentation on registered images. 
    '''
    # handle input
    df_img = basic.parse_tiff_reg(s_wd='tiff_registered/')

    # get slide_pxscene
    es_slidepxscene = set(df_img.slide_scene)
    if (len(es_slidepxscene) != 1):
        sys.exit(f'Error @ jinxif.galaxy.segment_cell_slidepxscene : more or less then one slide_pxscene found {sorted(es_slidepxscene)}.')
    s_slidepxscene = es_slidepxscene.pop()

    # get dapi image file name
    s_tiff_dapi = df_img.loc[(df_img.loc[:,'round'] == s_dapi_round) & (df_img.color == config.d_nconv['s_color_dapi_jinxif']) & (df_img.slide_scene == s_slidepxscene),:].index[0]

    # function call
    segment._make_segment_cell_zstack(
        s_slide_pxscene = s_slidepxscene,
        s_tiff_dapi = s_tiff_dapi,
        i_cell_diam = i_cell_diam,
        es_seg_marker = es_seg_marker,
        es_rare_marker = es_rare_marker,
        # file system
        s_regpath = 'tiff_registered/',
        s_segpath = 'tiff_segmentation/',
        # gpu
        b_gpu = b_gpu,
    )


# run from the command line
if __name__ == '__main__':

    # specify command line argument
    parser = argparse.ArgumentParser(description='run jinxif.galaxy.segment_cell_slidepxscene.')
    parser.add_argument(
        '--celldiam',
        help='',
        type=int,
        #nargs='*', # bue: will turn the output into a list of strings.
    )
    parser.add_argument(
        '--dapiround',
        help='',
        type=str,
        #nargs='*', # bue: will turn the output into a list of strings.
    )
    parser.add_argument(
        '--segmarker',
        help='',
        type=str,
        nargs='*', # bue: will turn the output into a list of strings.
    )
    parser.add_argument(
        '--raremarker',
        help='',
        type=str,
        nargs='*', # bue: will turn the output into a list of strings.
    )  
    parser.add_argument(
       '--gpu',
       help='',
       type=str,
       default='false',
       #nargs=1, # bue: will turn the output into a list of strings.
    )
    args = parser.parse_args()
    print('i_cell_diam:', args.celldiam, type(args.celldiam))
    print('s_dapi_round:', args.dapiround, type(args.dapiround))
    print('es_seg_marker:', args.segmarker, type(args.segmarker))
    print('es_rare_marker:', args.raremarker, type(args.raremarker))
    print('s_gpu:', args.gpu, type(args.gpu))

    # run code
    b_gpu = False
    if args.gpu in {'true', 'True'}:
        b_gpu = True
    segment_cell_slidepxscene(
        i_cell_diam = args.celldiam,
        s_dapi_round = args.dapiround,
        es_seg_marker = args.segmarker,
        es_rare_marker = args.raremarker,
        b_gpu = b_gpu,
    )

