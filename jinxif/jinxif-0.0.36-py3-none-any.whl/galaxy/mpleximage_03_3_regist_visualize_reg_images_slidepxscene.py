#####
# title: mpleximage_03_3_regist_visualize_reg_images_slidepxscene.py
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
def regist_visualize_reg_images(
        s_color,
    ):
    '''
    input: 
      regsitered image tiff files unter the input directory.
      s_color: string label for microscopy channel as specified in the 
          naming convention conform filename.

    output:
      png qualtiy controll plots under the output directory.

    description:
      generate a plot for the requested microscopy channel, 
      for each slide_scene with every rounds images for that channel.
    '''
    df_img_slide = basic.parse_tiff_reg(s_wd='tiff_registered/')
    print(df_img_slide)
    for s_slide_pxscene in sorted(df_img_slide.slide_scene.unique()):

        # generate output path and filename
        s_pathfile = f'png_qc/{s_slide_pxscene}_{s_color}_reg.png'
        print(s_pathfile)

        # filter data
        df_img_slidepxscene = df_img_slide.loc[
            (df_img_slide.color == s_color) & (df_img_slide.slide_scene == s_slide_pxscene),
            :
        ].sort_values('round_order')
        print(df_img_slidepxscene)
        df_img_slidepxscene.index.name = df_img_slide.index.name

        # generate figure
        jfplt.array_img_scatter(
            df_img = df_img_slidepxscene,
            s_xlabel = 'marker',
            ls_ylabel = ['markers','color'],
            s_title = 'round',
            s_title_main = 'slide_scene', # slide_mscene
            ti_array = (2, len(df_img_slidepxscene)//2 + 1),  # // is floor division
            ti_fig = (22,8),
            cmap = 'gray',
            s_pathfile = s_pathfile,
        )


# run from the command line
if __name__ == '__main__':

    # specify command line argument
    parser = argparse.ArgumentParser(description='run jinxif.galaxy.regist_visualize_reg_images.')
    parser.add_argument(
        'color',
        help='one color channel indetifier',
        type=str,
        #nargs=1, # bue: will turn the output into a list of strings.
    )

    args = parser.parse_args()
    print('s_color:', args.color)

    # run code
    regist_visualize_reg_images(
        s_color = args.color,  #'c1'
    )

