import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from pywt import cwt
from scipy.signal import resample

class SpectogramPlot():

    def __init__(self, consumer, channel='AF3', time_window=4, f_max=60, cmap='jet', frame_rate=5):

        self.sampling_rate = 976.5625
        self.n_levels = 256
        self.wavelet = 'cmor1.5-1.0'

        self.consumer = consumer
        self.frame_rate = frame_rate
        self.time_window = time_window
        self.f_max = f_max
        self.cmap = cmap

        self.channel = channel
        actual_channel_seq = ['AF3', 'FC3', 'C5', 'C3', 'CP3', 'PO3', 'Fz', 'Cz', 'PO4', 'CP4', 'C4', 'C6', 'FC4', 'AF4', 'CPz', 'Pz']
        self.channel_ind = actual_channel_seq.index(self.channel)

        self.num_updates = int(self.sampling_rate*self.time_window)
        self.update_window = 1/self.frame_rate
        self.downsample_to = int(self.f_max*time_window)
        self.dt = (1/self.f_max)
        self.scales =  np.arange(1, self.n_levels)

        self.num_xticks = time_window + 1
        self.num_yticks = int(self.f_max/10) + 1

    def set_up_plot(self, first_image):
        yticks = np.linspace(0, self.n_levels, self.num_yticks)
        yticklabels = np.around(np.linspace(self.f_max, 0, self.num_yticks), 1)

        xticks = np.linspace(0, self.downsample_to, self.num_xticks)
        self.xticklabels = np.around(np.linspace(0, self.time_window, self.num_xticks), 1)

        matplotlib.interactive(False)

        self.fig, self.axis = plt.subplots(1, figsize=(10, 6), num=f'Time-frequency plot for {self.channel}')
        
        self.fig.canvas.mpl_connect('close_event', self.on_close)
        self.axis.has_been_closed = False

        self.img_axis = self.axis.imshow(first_image, cmap=self.cmap)
        self.img_axis.set_clim(35, 95)

        self.axis.set_xticks(xticks) 
        self.axis.set_xticklabels(self.xticklabels, fontsize=12)
        self.axis.set_xlabel('Time (seconds)', fontsize=14)

        self.axis.set_yticks(yticks) 

        self.axis.set_yticklabels(yticklabels, fontsize=12)
        self.axis.set_ylabel('Frequency (Hertz)', fontsize=14)

        self.colorbar = plt.colorbar(self.img_axis, ax=self.axis)
        self.colorbar.ax.tick_params(labelsize=10) 
        self.colorbar.ax.set_title('Power (DB/Hz)',fontsize=14, fontweight='bold')

        plt.ion()
        plt.rcParams["font.weight"] = "bold"

    def on_close(self, event):
        event.canvas.figure.axes[0].has_been_closed = True

    def get_image(self, batch_data):
        channel_batch_data = resample(batch_data[self.channel_ind], self.downsample_to)
        coeffs, _ = cwt(channel_batch_data, self.scales, self.wavelet, self.dt)
        power = np.abs(coeffs)**2
        power_DB = 20*np.log10(power)
        return power_DB

    def show(self):

        first_batch_data = self.consumer.get_latest_data_packets(self.num_updates, 'default')
        first_image = self.get_image(first_batch_data)
        self.set_up_plot(first_image)

        while not self.axis.has_been_closed:
            t1 = time.process_time()
            while time.process_time() - t1 <= (self.update_window):
                continue
            t1 = time.process_time()
            new_batch_data = self.consumer.get_latest_data_packets(self.num_updates, 'default')
            new_image = self.get_image(new_batch_data)
            self.img_axis.set_data(new_image)
            self.xticklabels += self.update_window
            self.xticklabels = np.round(self.xticklabels, 1)
            self.axis.set_xticklabels(self.xticklabels, fontsize=12)
            self.fig.canvas.flush_events()
            plt.show()
    

if __name__ == '__main__':

    frame_rate = 5

    ###########Only for testing #######################
    class Consumer:
        def __init__(self):
            self.data = np.transpose(np.load('filtered_wet_data.npy'), axes=(1, 0))
            self.pointer = 0
            self.slide_by = int(967.5625/frame_rate)

        def get_latest_data_packets(self, bin_length, mode='default'):
            batch_data = self.data[:, self.pointer:self.pointer+bin_length]
            self.pointer += self.slide_by
            return batch_data

    consumer = Consumer()
    ##################################################
    
    spectrogram = SpectogramPlot(consumer, channel='AF4', time_window=5, f_max=60, cmap='jet', frame_rate=frame_rate)
    spectrogram.show()