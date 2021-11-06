import os

import numpy as np

from sknrf.settings import Settings
from sknrf.app.dataviewer.model.dataset import IQFile

header_map = {"sample_point": 2,
              "sample_rate": 10e6,
              "waveform_runtime_scaling": 1.0,
              "iq_modulation_filter": 40e6,
              "iq_output_filter": 40e6,
              "marker_1": "0-1",
              "marker_2": None,
              "marker_3": None,
              "marker_4": None,
              "pulse__rf_blanking": 4,
              "alc_hold": 3,
              "alc_status": "On",
              "bandwidth": "Auto",
              "power_search_reference": "Modulation"}
iq_array = np.asarray([1 + 0j], dtype=np.complex)
f = IQFile(os.sep.join((Settings().data_root, 'signals', 'CW.h5')), iq_array, header_map, mode='w')
sample_rate = [x['sample_rate'] for x in f.root.header.iterrows()][0]
f.close()

iq_array = np.random.normal(0, 1, [2 ** 15])
iq_array /= np.abs(iq_array).max()
f = IQFile(os.sep.join((Settings().data_root, 'signals', 'AWGN_real.h5')), iq_array, header_map, mode='w')
sample_rate = [x['sample_rate'] for x in f.root.header.iterrows()][0]
f.close()

iq_array = np.random.normal(0, 1, [2 ** 15]) + 1j * np.random.normal(0, 1, [2 ** 15])
iq_array /= np.abs(iq_array).max()
f = IQFile(os.sep.join((Settings().data_root, 'signals', 'AWGN.h5')), iq_array, header_map, mode='w')
sample_rate = [x['sample_rate'] for x in f.root.header.iterrows()][0]
f.close()