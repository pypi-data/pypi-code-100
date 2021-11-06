#####
# title: mpleximage_04_1_exposuretime_qc_batch.py
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
from jinxif import config
from jinxif import imgmeta
import os

# function
def exposuretime_qc_batch(
        s_batch,
    ):
    '''
    input:
        csv files under the exposuretime directory
        s_batch: batch label

    output:
        csv and png exposure time ms matrix file

    description:
        generate csv and png exposure time ms matrix file for exposure time error detetction.
    '''
    # get es_slide from filenames.
    es_slide = set()
    print(os.listdir('csv_exposuretime/'))
    for s_file in os.listdir('csv_exposuretime/'):
        print(f'file: {s_file}')
        ls_erase = config.d_nconv['s_format_csv_exposuretime'].split('{}')
        print(f'ls_erase: {ls_erase}')
        s_slide = s_file
        for s_erase in ls_erase:
            if (s_erase != ''):
                s_slide = s_slide.replace(s_erase,'')
        es_slide.add(s_slide)
    print(f'for batch {s_batch} detected slides: {sorted(es_slide)}')

    # call jinif function
    imgmeta._make_exposure_matrix(
        s_batch = s_batch,
        es_slide = es_slide,
        tr_figsize = None,
        s_metadir_input = 'csv_exposuretime/',
        s_metadir_output = 'csv_metaimages/',
    )


# run from the command line
if __name__ == '__main__':

    # specify command line argument
    parser = argparse.ArgumentParser(description='run jinxif.imgmeta.exposure_matrix.')
    parser.add_argument(
        'batch',
        help='',
        type=str,
        #nargs=1, # bue: will turn the output into a list of strings.
    )
    args = parser.parse_args()
    print('s_batch:', args.batch)

    # function call
    exposuretime_qc_batch(
        s_batch = args.batch,
    )

