import holoviews as hv
from holoviews.streams import Buffer

from streamz import Stream
from streamz.dataframe import DataFrame

from tornado.ioloop import PeriodicCallback
from tornado import gen

import pandas as pd
import numpy as np

from scipy.signal import resample, welch

class Timeplot:
    
    def __init__(self, upstream, time_window=3, channels=None, num_plot_columns=1, frame_rate=5, width=500, height=250, line_width=1.5, font_dict=None):
        
        self.upstream = upstream
        self.num_plot_columns = num_plot_columns
        self.width = width
        self.height = height
        self.line_width = line_width
        
        sampling_rate = 976.5625 
        downsample_by = 4
        
        channel_seq = ['AF3', 'FC3', 'C5', 'C3', 'CP3', 'PO3', 'Fz', 'Cz', 
                      'PO4', 'CP4', 'C4', 'C6', 'FC4', 'AF4', 'CPz', 'Pz']
        
        self.colors = ['deepskyblue', 'coral', 'blue', 'brown', 
                      'yellowgreen', 'red', 'olive', 'magenta', 
                      'maroon', 'peru', 'orchid', 'palevioletred',
                      'salmon', 'steelblue', 'seagreen', 'indianred']
        
        if not font_dict:
            self.font_dict = {'title': 14, 'labels': 12, 'xticks': 10, 'yticks': 10}
        else:
            self.font_dict = font_dict
        
        if not channels:
            self.channels = channel_seq
        else:
            self.channels = channels
            
        self.channel_inds = [channel_seq.index(channel) for channel in self.channels]
            
        self.x_axis_size = int((sampling_rate*time_window)/downsample_by)
        self.callback_period = 1000/frame_rate
        self.update_size = int(sampling_rate/frame_rate)
        self.downsample_to = int(self.update_size/downsample_by)
        
        self.downstream = Stream()
        
        example = pd.DataFrame({channel:[] for channel in self.channels}, index=[])
        
        self.df_downstream = DataFrame(self.downstream, example=example)
        
        self.cbdf = PeriodicCallback(self.emit, self.callback_period)
        
        self.create_layout()
        
    @staticmethod
    def x_tick_formatter(value):
        return str(value/250)
    
    @gen.coroutine
    def emit(self):
        
        if not self.upstream.status:
            self.stop()
        
        new_data = self.upstream.latest_data(self.update_size)
        
        new_data_downsampled = resample(new_data, self.downsample_to, axis=0)
        
        df_update = pd.DataFrame(new_data_downsampled[:, self.channel_inds], 
                                 columns=self.channels, 
                                 index=range(self.sample_pointer, self.sample_pointer+self.downsample_to))
        
        self.downstream.emit(df_update)
        
        self.sample_pointer +=  self.downsample_to
    
    def create_layout(self):
        dynamic_maps = []
    
        for i, channel in enumerate(self.channels):

            dynamic_map = hv.DynamicMap(hv.Curve, streams=[Buffer(self.df_downstream[channel], length=self.x_axis_size)]).opts(
                                                                    padding=0.1, width=self.width, height=self.height, 
                                                                    color = self.colors[i], title=channel,
                                                                    xlabel='x1000 samples', ylabel='uVolts',
                                                                    fontsize=self.font_dict, line_width=self.line_width, 
                                                                    xformatter=self.x_tick_formatter)

            dynamic_maps.append(dynamic_map)

        self.show = hv.Layout(dynamic_maps).cols(self.num_plot_columns)
    
    def start(self):
        self.sample_pointer = 0
        self.cbdf.start()
        
    def stop(self):
        self.cbdf.stop()
        

class PSDplot:
    
    def __init__(self, upstream, time_window=4, channels=None, freq_range=(0.5, 60), show_in_DB=True, common_axes=True, num_plot_columns=1, frame_rate=5, width=500, height=250, line_width=1.5, font_dict=None):
        
        self.upstream = upstream
        self.f_min, self.f_max =  freq_range
        self.show_in_DB = show_in_DB
        self.common_axes = common_axes
        self.num_plot_columns = num_plot_columns
        self.width = width
        self.height = height
        self.line_width = line_width
        
        sampling_rate = 976.5625 
        
        channel_seq = ['AF3', 'FC3', 'C5', 'C3', 'CP3', 'PO3', 'Fz', 'Cz', 
                      'PO4', 'CP4', 'C4', 'C6', 'FC4', 'AF4', 'CPz', 'Pz']
        
        self.colors = ['deepskyblue', 'coral', 'blue', 'brown', 
                      'yellowgreen', 'red', 'olive', 'magenta', 
                      'maroon', 'peru', 'orchid', 'palevioletred',
                      'salmon', 'steelblue', 'seagreen', 'indianred']
        
        if not font_dict:
            self.font_dict = {'title': 14, 'labels': 12, 'xticks': 10, 'yticks': 10}
        else:
            self.font_dict = font_dict
        
        if not channels:
            self.channels = channel_seq
        else:
            self.channels = channels
            
        self.channel_inds = [channel_seq.index(channel) for channel in self.channels]
        
        if self.show_in_DB:
            self.y_axis_unit = '(DB/hz)'
        else:
            self.y_axis_unit = '(uVolts^2)/hz'
            
        self.callback_period = 1000/frame_rate
        self.update_size = int(sampling_rate/frame_rate)
        
        self.new_fs = int(2*self.f_max) + 10
        self.downsample_to = int(self.new_fs*time_window)
        
        freqs, _ = welch(np.ones((self.downsample_to)), fs=self.new_fs, nperseg=self.downsample_to)
        self.show_freqs_at = (freqs >= self.f_min)*(freqs <= self.f_max)
        self.show_freqs = freqs[self.show_freqs_at]
        self.x_axis_size = len(self.show_freqs)
        
        self.downstream = Stream()
        
        example = pd.DataFrame({channel:[] for channel in self.channels}, index=[])
        
        self.df_downstream = DataFrame(self.downstream, example=example)
        
        self.cbdf = PeriodicCallback(self.emit, self.callback_period)
        
        self.create_layout()
        
    @gen.coroutine
    def emit(self):
        
        if not self.upstream.status:
            self.stop()
        
        new_batch = self.upstream.latest_data(self.update_size)
        
        downsampled_data = resample(new_batch[:, self.channel_inds], self.downsample_to, axis=0)
        
        _, batch_psd = welch(downsampled_data, fs=self.new_fs, nperseg=self.downsample_to, axis=0)
        
        batch_psd = batch_psd[self.show_freqs_at] 
        
        if self.show_in_DB:
            batch_psd = 20*np.log10(batch_psd + 1e-7)
            
        df_update = pd.DataFrame(batch_psd, columns=self.channels, index=self.show_freqs)
        
        self.downstream.emit(df_update)
    
    def create_layout(self):
        
        dynamic_maps = []
    
        for i, channel in enumerate(self.channels):

            dynamic_map = hv.DynamicMap(hv.Curve, streams=[Buffer(self.df_downstream[channel], length=self.x_axis_size)]).opts(
                                                                    padding=0.1, width=self.width, height=self.height, 
                                                                    color = self.colors[i], title=channel,
                                                                    xlabel='Frequency (hz)', ylabel=self.y_axis_unit,
                                                                    fontsize=self.font_dict)

            dynamic_maps.append(dynamic_map)

        self.show = hv.Layout(dynamic_maps).cols(self.num_plot_columns)
        
    def create_overlay(self):
        
        dynamic_maps = []
    
        for i, channel in enumerate(self.channels):

            dynamic_map = hv.DynamicMap(hv.Curve, streams=[Buffer(self.df_downstream[channel], length=self.x_axis_size)]).opts(
                                                                    padding=0.1, width=self.width, height=self.height, 
                                                                    color = self.colors[i], title=f"Power Spectral Density",
                                                                    xlabel='Frequency (hz)', ylabel=self.y_axis_unit,
                                                                    fontsize=self.font_dict)

            dynamic_maps.append(dynamic_map)

        self.show = hv.Overlay(dynamic_maps).collate()
    
    def start(self):
        self.cbdf.start()
        if self.common_axes:
            self.create_overlay()
        else:
            self.create_layout()
        
    def stop(self):
        self.cbdf.stop()


class Bandpowerplot:
    
    def __init__(self, upstream, time_window=4, band_dict=None, bands=None, channels=None, show_absolute=False, frame_rate=5, width=500, height=250, font_dict=None):
        
        self.upstream = upstream
        self.show_absolute = show_absolute
        self.width = width
        self.height = height
        
        sampling_rate = 976.5625 
        
        channel_seq = ['AF3', 'FC3', 'C5', 'C3', 'CP3', 'PO3', 'Fz', 'Cz', 
                      'PO4', 'CP4', 'C4', 'C6', 'FC4', 'AF4', 'CPz', 'Pz']
        
        if not band_dict:
            self.band_dict = {'delta' : (0.5, 4),
                              'theta' : (4, 8),
                              'alpha' : (8, 13),
                              'beta'  : (13, 32),
                              'gamma' : (32, 60)}
        else:
            self.band_dict = band_dict
            
        if not bands:
            self.bands = self.band_dict.keys()
        else:
            self.bands = bands
        
        if not font_dict:
            self.font_dict = {'title': 14, 'labels': 12, 'xticks': 10, 'yticks': 10}
        else:
            self.font_dict = font_dict
        
        if not channels:
            self.channels = channel_seq
        else:
            self.channels = channels
            
        self.channel_inds = [channel_seq.index(channel) for channel in self.channels]
        
        if self.show_absolute:
             self.y_axis_unit = 'Power (microVolts^2)'
        else:
            self.y_axis_unit = '% Composition'
            
        self.callback_period = 1000/frame_rate
        self.update_size = int(sampling_rate/frame_rate)
        
        self.f_min = min([min(f_range) for f_range in self.band_dict.values()])
        self.f_max = max([max(f_range) for f_range in self.band_dict.values()])
        
        self.new_fs = int(2*self.f_max) + 10
        self.downsample_to = int(self.new_fs*time_window)
        
        freqs, _ = welch(np.ones((self.downsample_to)), fs=self.new_fs, nperseg=self.downsample_to)
        
        self.band_inds = []
        for f_range in self.band_dict.values():
            self.band_inds.append(np.intersect1d(np.where(freqs >= f_range[0]), np.where(freqs < f_range[1])))
        
        self.downstream = Stream()
        
        example = pd.DataFrame({'Frequency band':self.bands, self.y_axis_unit:[0 for band in self.bands]}, index=range(len(self.bands)))
        example = example.set_index('Frequency band')
        
        self.df_downstream = DataFrame(self.downstream, example=example)
        
        self.cbdf = PeriodicCallback(self.emit, self.callback_period)
        
        self.create_barchart()
        
    @gen.coroutine
    def emit(self):
        
        if not self.upstream.status:
            self.stop()
            
        new_batch = self.upstream.latest_data(self.update_size)
        
        downsampled_data = resample(new_batch[:, self.channel_inds], self.downsample_to, axis=0)
        
        _, batch_psd = welch(downsampled_data, fs=self.new_fs, nperseg=self.downsample_to, axis=0)
        
        avg_psd = np.mean(batch_psd, axis=1)
        
        band_powers = []
        
        for inds in self.band_inds:
            band_powers.append(np.sum(avg_psd[inds]))
            
        if not self.show_absolute:
            total_power = sum(band_powers)*1e-2
            band_powers = [bp/total_power for bp in band_powers]
            
        df_update = pd.DataFrame({'Frequency band':self.bands, self.y_axis_unit:band_powers}, index=range(len(self.bands)))
        df_update = df_update.set_index('Frequency band')
        
        self.downstream.emit(df_update)
    
    def create_barchart(self):
        
        self.show = hv.DynamicMap(hv.Bars, streams=[Buffer(self.df_downstream[self.y_axis_unit], length=len(self.bands))]).opts(
                                                            padding=0.1, width=self.width, height=self.height, title='Bandpower',
                                                            fontsize=self.font_dict)

    def start(self):
        self.cbdf.start()
        
    def stop(self):
        self.cbdf.stop()
        