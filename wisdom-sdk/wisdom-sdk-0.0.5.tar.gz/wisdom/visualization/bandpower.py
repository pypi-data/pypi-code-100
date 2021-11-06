import sys
from PyQt5.QtChart import QChart, QChartView, QHorizontalBarSeries, QBarSet, QBarCategoryAxis
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import QObject, pyqtSignal, QTimer
import numpy as np
from scipy.signal import resample, welch

class BandpowerPlot:
    def __init__(self, consumer, consider_channels=None, time_window=4, frame_rate=10, show_bands=None, min_freq=0.5, max_freq=60, plot_absolute=False):

        self.consumer = consumer
        self.consider_channels = consider_channels
        self.time_window = time_window
        self.frame_rate = frame_rate
        self.show_bands = show_bands
        self.min_freq = min_freq
        self.max_freq = max_freq
        self.plot_absolute = plot_absolute

    def show(self):
        self.app = QApplication(sys.argv)
        self.window = Bandpower_mainWindow(self.consider_channels, self.time_window, self.show_bands, self.min_freq, self.max_freq, self.plot_absolute)
        self.window.show()
        data_producer = Bandpower_dataProducer(self.consumer, self.time_window, self.frame_rate)
        data_producer.dataChanged.connect(lambda x :self.window.update_plot(x))
        sys.exit(self.app.exec_())

class Bandpower_mainWindow(QMainWindow):
    def __init__(self, consider_channels, time_window, show_bands, min_freq, max_freq, plot_absolute):
        super().__init__()

        band_dict = {'delta' : (min_freq, 4),
                    'theta' : (4, 8),
                    'alpha' : (8, 13),
                    'beta'  : (13, 32),
                    'gamma' : (32, max_freq)}

        if not show_bands:
            show_bands = list(band_dict.keys())

        self.band_dict = {band:f_range for band, f_range in band_dict.items() if band in show_bands}

        self.f_max = max([max(f_range) for f_range in self.band_dict.values()])

        self.old_fs = 976.5625
        self.binLen = int(self.old_fs*time_window)

        self.new_fs = int(2*self.f_max) + 10
        self.downsample_to = int(self.new_fs*time_window)

        freqs, _ = welch(np.ones((self.downsample_to)), fs=self.new_fs, nperseg=self.downsample_to, axis=-1)

        actual_channel_seq = ['AF3', 'FC3', 'C5', 'C3', 'CP3', 'PO3', 'Fz', 'Cz', 'PO4', 'CP4', 'C4', 'C6', 'FC4', 'AF4', 'CPz', 'Pz']
        if not consider_channels:
            consider_channels = actual_channel_seq

        self.n_channels = len(consider_channels)
        self.channels_inds = [actual_channel_seq.index(channel) for channel in consider_channels]

        self.band_inds = []
        for freq_range in self.band_dict.values():
            self.band_inds.append(np.intersect1d(np.where(freqs >= freq_range[0]), np.where(freqs < freq_range[1])))

        chartview = self.create_barchart()

        self.setGeometry(200, 200, 1400, 600)

        layout = QVBoxLayout()
        layout.addWidget(chartview)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.plot_absolute = plot_absolute

        if not self.plot_absolute:
            axisX = self.chart.axisX(self.series)
            axisX.setMin(0)
            axisX.setMax(1)
            axisX.setTitleText("Bandpower precentage composition")

    def create_barchart(self):
        self.set = QBarSet('Bandpower')
        self.set.append([0 for _ in range(len(self.band_dict))])
        self.series = QHorizontalBarSeries()
        self.series.append(self.set)

        self.chart = QChart()
        self.chart.setTitle('Realtime Bandpower Bargraph')
        self.chart.addSeries(self.series)

        axisY = QBarCategoryAxis()
        axisY.append([band for band in self.band_dict])
        self.chart.createDefaultAxes()
        self.chart.setAxisY(axisY, self.series)

        self.chart.legend().hide()
        chartview = QChartView(self.chart)

        return chartview

    def update_plot(self, new_data):

        new_data_downsampled = resample(new_data[self.channels_inds], self.downsample_to, axis= 1)
        _, psd = welch(new_data_downsampled, fs=self.new_fs, nperseg=self.downsample_to, axis=1)
        avg_psd = np.mean(psd, axis=0)

        band_powers = []

        for inds in self.band_inds:
            band_powers.append(np.sum(avg_psd[inds]))

        if not self.plot_absolute:
            total_power = sum(avg_psd)
            band_powers = [bp/total_power for bp in band_powers]

        else:
            axisX = self.chart.axisX(self.series)
            axisX.setMin(0)
            axisX.setMax(max(band_powers)*1.2)
            axisX.setTitleText("Absolute Bandpower (microVolts^2)")

        for b in range(len(self.band_dict)):
            self.set.replace(b, band_powers[b])

class Bandpower_dataProducer(QObject):

    dataChanged = pyqtSignal(np.ndarray)

    def __init__(self, consumer, time_window, frame_rate):
        super().__init__()

        old_fs = 976.5625
        self.updateTime = int(1000/frame_rate) 
        self.consumer = consumer
        self.bin_length = int(old_fs*time_window)
        QTimer.singleShot(self.updateTime, self.send_data)

    def send_data(self):
        new_data = self.consumer.get_latest_data_packets(self.bin_length, 'default')
        self.dataChanged.emit(new_data)
        QTimer.singleShot(self.updateTime, self.send_data)

if __name__ == "__main__":

    frame_rate = 4

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

    bp_plot = BandpowerPlot(consumer, consider_channels=None, time_window=4, frame_rate=frame_rate, show_bands=['theta', 'alpha', 'beta', 'gamma'], min_freq=0.5, max_freq=60, plot_absolute=False)
    bp_plot.show()