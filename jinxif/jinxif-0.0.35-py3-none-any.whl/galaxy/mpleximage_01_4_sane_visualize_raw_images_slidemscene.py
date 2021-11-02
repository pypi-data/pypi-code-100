#####
# title: mpleximage_01_4_sane_visualize_raw_images_slidemscene.py
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
from jinxif import jfplt

# function
def sane_visualize_raw_images(
        s_color,
    ):
    '''
    input: 
      raw images tiff files unter the input directory.
      s_color: string label for microscopy channel as specified in the 
          naming convention conform filename.

    output:
      png qualtiy controll plots under the output directory.

    description:
      generate a plot for the requested microscopy channel, 
      for each slide_scene with every rounds images for that channel.
    '''
    df_img_slide = basic.parse_tiff_raw('tiff_raw/')
    print(df_img_slide)
    for s_slide_mscene in sorted(df_img_slide.slide_mscene.unique()):

        # generate output path and filename
        s_pathfile = f'png_qc/{s_slide_mscene}_{s_color}_raw.png'
        print(s_pathfile)

        # filter data
        df_img_slidemscene = df_img_slide.loc[
            (df_img_slide.color == s_color) & (df_img_slide.slide_mscene == s_slide_mscene),
            :
        ].sort_values('round_order')
        print(df_img_slidemscene)
        df_img_slidemscene.index.name = df_img_slide.index.name

        # generate figure
        jfplt.array_img_scatter(
            df_img = df_img_slidemscene,
            s_xlabel = 'marker',
            ls_ylabel = ['markers','color'],
            s_title = 'round',
            s_title_main = 'slide_mscene', # slide_scene
            ti_array = (2, len(df_img_slidemscene)//2 + 1),  # // is floor division
            ti_fig = (22,8),
            cmap = 'gray',
            s_pathfile = s_pathfile,
        )


# run from the command line
if __name__ == '__main__':

    # specify command line argument
    parser = argparse.ArgumentParser(description='run jinxif.galaxy.sane_visualize_raw_images.')
    parser.add_argument(
        'color',
        help='',
        type=str,
        nargs='+', # bue: will turn the output into a list of strings.
    )

    args = parser.parse_args()
    print('ls_color:', args.color)

    # run code
    for s_color in args.color: #['c1']
        sane_visualize_raw_images(
            s_color = s_color
        )

