#####
# title: mpleximage_02_1_imgmeta_fetch_meta_slide.py
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
import argparse
from jinxif import basic
from jinxif import config
from jinxif import imgmeta


# function
def fetch_meta_slide(
        s_sceneposition_round,
    ):
    '''
    input: 
      czi files unter the original input directory.
      czi files unter the splitscene input directory.

    output:
      csv data files under the exposure time output directory.
      csv data file under the scene position output directory.

    description:
      generate a plot for the requested microscopy channel, 
      for each slide_scene with every rounds images for that channel.
    '''
    # fetch exposure time
    # get path parse czi file name
    df_img_splitmscene = basic.parse_czi_splitscene(s_wd = 'czi_splitscene/')


    if (df_img_splitmscene.shape[0] != 0):
        # slide with one or many scenes
        imgmeta.fetch_meta_slide_exposuretime(
            df_img = df_img_splitmscene,
            s_metadir = 'csv_exposuretime/',
        )

    else:
        # get path parse czi file name
        df_img_original = basic.parse_czi_original(s_wd = 'czi_original/')
        # slide with one or many scenes
        imgmeta.fetch_meta_slide_exposuretime(
            df_img = df_img_original,
            s_metadir = 'csv_exposuretime/',
        )

    # fetch scene position
    # slide with one or many scenes
    imgmeta.fetch_meta_slide_sceneposition(
        s_slide = None,
        s_czidir_original = 'czi_original/',
        s_sceneposition_round = s_sceneposition_round,
        s_metadir = 'csv_sceneposition/',
    )



# run from the command line
if __name__ == '__main__':
    # specify command line argument
    parser = argparse.ArgumentParser(description='run jinxif.imgmeta.fetch_meta_slide')
    parser.add_argument(
        'round',
        help='',
        type=str,
        #nargs=1, # bue: will turn the output into a list of strings.
    )
    args = parser.parse_args()
    print('s_sceneposition_round:', args.round)

    # function call
    fetch_meta_slide(
        s_sceneposition_round = args.round, # 'R1_'
    )

