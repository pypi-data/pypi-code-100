########
# title: template_filterfeatures_slide.py
#
# author: Jenny, bue
# license: GPLv>=3
# version: 2021-07-05
#
# description:
#     template script for python base, marker dependent cell segmenation based feature filter.
#
# instruction:
#     use jinxif.feat.filter_feature_spawn function to generate and run executables from this template.
#####

# libraries
from jinxif import _version
from jinxif import feat
import resource
import time

# set variables
poke_s_slide = 'peek_s_slide'
poke_es_dapipartition_filter = peek_es_dapipartition_filter
poke_i_thresh_manual = peek_i_thresh_manual
poke_s_thresh_marker = 'peek_s_thresh_marker'
if (poke_s_thresh_marker == 'None'):
    poke_s_thresh_marker = None
poke_i_exp = peek_i_exp
poke_i_mem = peek_i_mem
poke_i_shrink = peek_i_shrink
poke_es_marker_needed = peek_es_marker_needed
poke_es_cytoplasm_marker = peek_es_cytoplasm_marker
poke_es_custom_markerpartition = peek_es_custom_markerpartition
poke_es_shrink_marker = peek_es_shrink_marker
poke_b_filter_na = peek_b_filter_na
poke_ds_shape = peek_ds_shape
poke_ds_centroid = peek_ds_centroid
poke_s_afsubdir = 'peek_s_afsubdir'
poke_s_segdir = 'peek_s_segdir'
poke_s_format_segdir_cellpose = 'peek_s_format_segdir_cellpose'
poke_s_qcdir = 'peek_s_qcdir'

# off we go
print(f'run jinxif.feat.filter_features on {poke_s_afsubdir} {poke_s_slide} ...')
r_time_start = time.time()

# filter features
feat.filter_features(
    s_slide = poke_s_slide,
    es_dapipartition_filter = poke_es_dapipartition_filter, # {'DAPI1_nuclei','DAPI2_nuclei','DAPI16_nuclei'},
    i_thresh_manual = poke_i_thresh_manual, # 1000,
    s_thresh_marker = poke_s_thresh_marker, # 'Ecad'
    i_exp = poke_i_exp, # 5
    i_mem = poke_i_mem, # 2
    i_shrink = poke_i_shrink, #0
    es_marker_needed = poke_es_marker_needed, #  {'DAPI16','Ecad'},
    es_cytoplasm_marker = poke_es_cytoplasm_marker, # {'Ecad'} cancer marker
    es_custom_markerpartition = poke_es_custom_markerpartition,  # optional
    es_shrink_marker = poke_es_shrink_marker, # optional against bleed throgh list of shrunken marker that should replace nucleus, exp{i_exp}, perinuc{i_exp}, or cytoplasm.
    b_filter_na = poke_b_filter_na,
    ds_shape = poke_ds_shape,
    ds_centroid = poke_ds_centroid,
    s_afsubdir = poke_s_afsubdir,
    s_segdir = poke_s_segdir,
    s_format_segdir_cellpose = poke_s_format_segdir_cellpose,  # s_segdir, s_slide
    s_qcdir = poke_s_qcdir,
)

# rock to the end
r_time_stop = time.time()
print('done jinxif.feat.filter_features!')
print(f'run time: {(r_time_stop - r_time_start) / 3600}[h]')
print(f'run max memory: {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000000}[GB]')
print('you are running jinxif version:', _version.__version__)
