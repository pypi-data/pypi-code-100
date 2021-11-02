#####
# title: mpleximage_03_2_sane_tiff_reg_slide.py
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
from jinxif import basic
from jinxif import config
from jinxif import sane


# function
def sane_tiff_registered():
    '''
    input: tiff files unter the input directory.
    output: stdout about slide wide filename nameing convention status.

    description:
        check standar filenameing convention, as specified in jinxif config, 
        on a singl tiff_registered galaxy data collection.
    '''
    df_img_slide = basic.parse_tiff_reg('tiff_registered/')
    sane.count_images(
        df_img = df_img_slide
    )
    sane.check_markers(
        df_img = df_img_slide, 
        es_markerdapiblank_standard = config.es_markerdapiblank_standard,
        es_markerpartition_standard = config.es_markerpartition_standard,
    )


# run from the command line
if __name__ == '__main__':

    # run code
    sane_tiff_registered()
