from scipy import signal
from wisdom.utils import *
import matplotlib.pyplot as plt
import numpy as np


class Filters:
    def __init__(self):
        self.filters = []

    def add_filter(self, filter_obj, index=None):
        if isinstance(filter_obj, Filter):
            if index is None:
                self.filters.append(filter_obj)
            else:
                self.filters.insert(index, filter_obj)
        else:
            raise ValueError("Pass a valid Filter Object")

    def get_filters(self):
        return self.filters

    def remove_filter(self, index):
        self.filters.pop(index)
        print(f"Removed Filter at index {index}")


class Filter:
    def __init__(self, filter_type, response_type, cutoff_freqs, bands, filter_coeffs, info, initial_state):
        self.filter_type = filter_type
        self.response_type = response_type
        self.cutoff_freqs = cutoff_freqs
        self.bands = bands
        self.filter_coeffs = filter_coeffs
        self.additional_information = info
        self.init_state = initial_state

    def print_summary(self):
        print("=====================")
        print(f"Filter Type : {self.filter_type}")
        print(f"Response Type : {self.response_type}")
        print(f"Cutoff Frequencies : {self.cutoff_freqs}")
        print(f"Band/s Information : {self.bands}")
        print(f"Additional Information : {self.additional_information}")

    def plot_complete_response(self, sfreq=SAMPLING_FREQUENCY):
        w, h = signal.sosfreqz(self.filter_coeffs, worN=8192)
        fig, ax1 = plt.subplots()
        ax1.set_title('Digital filter frequency response')
        ax1.plot(w * sfreq / (2 * np.pi), 20 * np.log10(abs(h)), 'b')
        ax1.set_ylabel('Amplitude [dB]', color='b')
        ax1.set_xlabel('Frequency [Hz]')
        ax2 = ax1.twinx()
        angles = np.unwrap(np.angle(h))
        ax2.plot(w * sfreq / (2 * np.pi), angles, 'g')
        ax2.set_ylabel('Angle (radians)', color='g')
        ax2.grid()
        ax2.axis('tight')
        plt.show()
