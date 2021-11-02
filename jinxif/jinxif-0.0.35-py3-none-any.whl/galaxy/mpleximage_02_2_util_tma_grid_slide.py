#####
# title: mpleximage_02_2_util_tma_grid_slide.py
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
from jinxif import util

# function
def tma_grid(
        s_slide,
        i_core_yaxis,
        i_core_xaxis,
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
    # call jinif function
    if (i_core_yaxis == 0):
        i_core_yaxis = None
    if (i_core_xaxis == 0):
        i_core_xaxis = None
    util.tma_grid(
        s_slide = s_slide,
        i_core_yaxis = i_core_yaxis,
        i_core_xaxis = i_core_xaxis,
        r_sampler = 0.98,
        s_metadir = 'csvpng_metaimages/',
    )


# run from the command line
if __name__ == '__main__':

    # specify command line argument
    parser = argparse.ArgumentParser(description='run jinxif.util.tma_grid.')
    parser.add_argument(
        'slide',
        help='',
        type=str,
        #nargs=1, # bue: will turn the output into a list of strings.
    )
    parser.add_argument(
        '-y',
        help='',
        type=int,
    )
    parser.add_argument(
        '-x',
        help='',
        type=int,
    )
    args = parser.parse_args()
    print('s_slide:', args.slide)
    print('i_core_yaxis:', args.y)
    print('i_core_xaxis:', args.x)

    # function call
    tma_grid(
        s_slide = args.slide,
        i_core_yaxis = args.y,
        i_core_xaxis = args.x,
    )

