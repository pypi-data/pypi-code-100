#####
# title: mpleximage_10_1_segmentation_nuccell_zproj_label_qc.py
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
from jinxif import thresh
from jinxif import config
import pandas as pd
import sys

# function
def segmentation_nuccell_zprojlabel_qc_slidepxscene(
        s_input,
    ):
    '''
    input:
      s_input: are the images in tiff_registered_input registeredimages 
          or auto fluorescent subtractedregisterdimages?
      registered or autofluorescent subtracted registered images under the input directory.

    output:
      autotreshold csv file added to the input directory.

    description:
      calcualtes autothreshold and generates a csv summary file per slide_pxscene, all markers.
    '''

    # function call
    df_thresh = pd.DataFrame()
    thresh._make_auto_thresh(
        s_afsubpath = 'tiff_registered/',
        df_thresh = df_thresh,
    )

    # get slide_pxscene
    es_slidepxscene = set(df_thresh.slide_scene)
    if (len(es_slidepxscene) != 1):
        sys.exit(f'Error jinxif.galaxy.segmentation_nuccell_zprojlabel_qc_slidepxscene : more or less then one slide_pxscene found {sorted(es_slidepxscene)}.')
    s_slidepxscene = es_slidepxscene.pop()

    # write to file
    s_ofile = config.d_nconv['s_format_csv_threshold'].format(s_slidepxscene, s_input)
    df_thresh.index.name = s_input
    df_thresh.to_csv('csv_metaimages/' + s_ofile)
    print(f'write file: csv_metaimages/{s_ofile}')


# run from the command line
if __name__ == '__main__':

    # specify command line argument
    parser = argparse.ArgumentParser(description='run jinxif.galaxy.segmentation_nuccell_zprojlabel_qc_slidepxscene.')
    parser.add_argument(
       '--imagetype',
       help='',
       type=str,
       default='registeredimages',
       #nargs=1, # bue: will turn the output into a list of strings.
    )
    args = parser.parse_args()
    print('s_input:', args.imagetype, type(args.imagetype))

    # run code
    segmentation_nuccell_zprojlabel_qc_slidepxscene(
        s_input=args.imagetype,
    )
