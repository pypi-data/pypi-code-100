#####
# title: mpleximage_05_1_basic_marker_table_slidepxscene.py
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

# function
def basic_marker_table_batch(
        s_batch,
    ):
    '''
    input: 
      registered image tiff files unter the input directory.
      s_batch: batch id.

    output:
      csv round channel marker table.

    description:
      generate a round channel marker table. 
    '''
    # parse filenames for one registered slidepxscene
    df_img_slidepxscene = basic.parse_tiff_reg(s_wd='tiff_registered/')
    print(df_img_slidepxscene.info())

    # generate table
    basic._make_marker_table(
        df_img = df_img_slidepxscene,
        s_batch = s_batch,
        s_regpath = 'csv_metaimages/',
    )


# run from the command line
if __name__ == '__main__':

    # specify command line argument
    parser = argparse.ArgumentParser(description='run jinxif.galaxy.basic_marker_table_batch.')
    parser.add_argument(
        'batch',
        help='',
        type=str,
        #nargs=1, # bue: will turn the output into a list of strings.
    )
    args = parser.parse_args()
    print('s_batch:', args.batch)

    # run code
    basic_marker_table_batch(
        s_batch = args.batch,
    )
