#####
# title: mpleximage_10_1_segmentation_nuccell_zproj_label_qc_slidepxscene.py
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
#import argparse
from jinxif import segment

# function
def segmentation_nuccell_zprojlabel_qc_slidepxscene():
    '''
    input: 
      nucleus and cell segementaion basin label tiff file unter the input directory.
      nucleus and cell zprojection png file unter the input directory.

    output:
      nucleus and cell zprojection and segementaion basin label qc plot.

    description:
      generate qc png plotf for nucleus and cell zprojection and segementaion basin label files.
    '''
    # function call
    segment._make_nuccell_zprojlabel_imgs(
        # file system
        s_segpath = 'segmentation/',
        s_qcpath = 'output/',
    )


# run from the command line
if __name__ == '__main__':

    # specify command line argument
    #parser = argparse.ArgumentParser(description='run jinxif.galaxy.segmentation_nuccell_zprojlabel_qc_slidepxscene.')

    # run code
    segmentation_nuccell_zprojlabel_qc_slidepxscene()
