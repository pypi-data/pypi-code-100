import sys
from PyQt5.QtChart import QLineSeries, QChart, QChartView, QValueAxis
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QPointF, QObject, pyqtSignal, QTimer
import numpy as np
from scipy.signal import resample, welch

class PSDplot:
    def __init__(self, consumer, show_channels=None, time_window=4, frame_rate=10, freq_range=(0.5, 60), plot_in_decibels=True):
 
        self.consumer = consumer
        self.show_channels = show_channels
        self.time_window = time_window
        self.frame_rate = frame_rate
        self.freq_range = freq_range
        self.plot_in_decibels = plot_in_decibels
        
    def show(self):
        self.app = QApplication(sys.argv)
        self.window = PSD_mainWindow(self.show_channels, self.time_window, self.freq_range, self.plot_in_decibels)
        self.window.show()
        data_producer = PSD_dataProducer(self.consumer, self.time_window, self.frame_rate)
        data_producer.dataChanged.connect(lambda x :self.window.update_plot(x))
        sys.exit(self.app.exec_())

class PSD_mainWindow(QMainWindow):
    def __init__(self, show_channels, time_window, freq_range, plot_in_decibels):
        super().__init__()

        self.old_fs = 976.5625
        self.binLen =  int(self.old_fs*time_window)
        self.plot_in_decibels = plot_in_decibels

        self.f_min, self.f_max = freq_range
        self.new_fs = int(2*self.f_max) + 10
        self.downsample_to = int(self.new_fs*time_window)

        freqs, _ = welch(np.ones((self.downsample_to)), fs=self.new_fs, nperseg=self.downsample_to)
        self.show_freqs = (freqs >= self.f_min)*(freqs <= self.f_max)
        self.spectrum_len = np.count_nonzero(self.show_freqs)

        actual_channel_seq = ['AF3', 'FC3', 'C5', 'C3', 'CP3', 'PO3', 'Fz', 'Cz', 'PO4', 'CP4', 'C4', 'C6', 'FC4', 'AF4', 'CPz', 'Pz']
        if not show_channels:
            show_channels = actual_channel_seq

        self.channel_names = show_channels
        self.n_channels = len(show_channels)
        self.channels_inds = [actual_channel_seq.index(channel) for channel in show_channels]

        self.plot_in_decibels = plot_in_decibels

        self.chart = QChart()
        self.chart.setTitle('Realtime Power Spectral Density plot')
        
        self.axisX = QValueAxis()
        self.axisX.setRange(self.f_min, self.f_max)
        self.axisX.setTitleText("Frequency (Hz)")

        self.axisY = QValueAxis()
        self.axisY.setRange(0, 100)
        if self.plot_in_decibels:
            self.axisY.setTitleText("PSD (DB/Hz)")
        else:
            self.axisY.setTitleText("PSD (microVolts^2/Hz)")

        self.chart.addAxis(self.axisX, Qt.AlignBottom)
        self.chart.addAxis(self.axisY, Qt.AlignLeft)

        for n in range(self.n_channels):
            self.add_series(n)

        self.chart.legend().setVisible(True)
        
        chartview = QChartView(self.chart)

        self.xVals = np.linspace(self.f_min, self.f_max, self.spectrum_len)

        self.setGeometry(200, 200, 1400, 600)

        layout = QVBoxLayout()
        layout.addWidget(chartview)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def add_series(self, n):
        setattr(self, f'series{n}', QLineSeries())
        series = getattr(self, f'series{n}')
        series.setName(self.channel_names[n])
        self.chart.addSeries(series)
        series.attachAxis(self.axisX)
        series.attachAxis(self.axisY)

    def update_plot(self, new_data):

        new_data_downsampled = resample(new_data[self.channels_inds], self.downsample_to, axis= 1)
        _, psd = welch(new_data_downsampled, fs=self.new_fs, nperseg=self.downsample_to, axis=1)

        if self.plot_in_decibels:
            psd = 20*np.log10(psd[:, self.show_freqs])

        y_max = np.max(psd) + 5
        y_min  = np.min(psd) - 5

        self.axisY.setRange(y_min, y_max)

        for n in range(self.n_channels):
            series = getattr(self, f'series{n}')
            series.clear()

            for i in range(self.spectrum_len):
                series.append(QPointF(self.xVals[i], psd[n, i]))

class PSD_dataProducer(QObject):

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

    frame_rate = 10

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

    psdplot = PSDplot(consumer, show_channels=['PO3', 'PO4'], time_window=4, frame_rate=frame_rate, freq_range=(4, 60), plot_in_decibels=True)
    psdplot.show()