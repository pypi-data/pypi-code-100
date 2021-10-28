import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from scipy.interpolate import CloughTocher2DInterpolator

class HeadPlot():

    def __init__(self, consumer, cmap='jet', frame_rate=5):

        self.consumer = consumer
        self.sampling_rate = 976.5625
        self.image_shape = (128, 128)
        self.frame_rate = frame_rate

        self.num_updates = int(self.sampling_rate/self.frame_rate)
        self.frame_duration = 1/self.frame_rate

        channel_locs = pd.read_csv('channel_locs.csv', index_col='channel')
        x = channel_locs['x'].values.astype(int)
        y = channel_locs['y'].values.astype(int)
        x_annotation = channel_locs['x_annotation'].values.astype(int)
        y_annotation = channel_locs['y_annotation'].values.astype(int)
        channels = channel_locs.index.to_list()

        self.coordinates = ((x, y))
        self.x_grid, self.y_grid = np.meshgrid([i for i in range(self.image_shape[0])], [i for i in range(self.image_shape[1])])

        matplotlib.interactive(False)
        self.cmap = matplotlib.cm.get_cmap(cmap).copy()
        self.cmap.set_bad(color='white')

        self.fig, self.axis = plt.subplots(1, figsize=(10, 7), num='Topographical headplot')
        
        self.fig.canvas.mpl_connect('close_event', self.on_close)
        self.axis.has_been_closed = False

        self.axis.scatter(x, y)

        for x_ann, y_ann, channel in zip(x_annotation, y_annotation, channels):
            self.axis.annotate(channel, (x_ann, y_ann), fontsize=12, fontweight='bold')

        initial_random_batch_data = np.random.normal(loc=0.0, scale=200, size=(16, self.num_updates))

        initial_random_image = self.get_image(initial_random_batch_data)

        self.img_axis = self.axis.imshow(initial_random_image, cmap=self.cmap)

        plt.ion()
        plt.axis('off')
        plt.rcParams["font.weight"] = "bold"

        self.colorbar = plt.colorbar(self.img_axis, ax=self.axis)
        self.colorbar.ax.tick_params(labelsize=10) 
        self.colorbar.ax.set_title('microVolts',fontsize=12, fontweight='bold')

    def on_close(self, event):
        event.canvas.figure.axes[0].has_been_closed = True

    def get_image(self, batch_data):
        batch_mean = np.mean(batch_data, axis=1)
        interpolator = CloughTocher2DInterpolator(self.coordinates, batch_mean, fill_value=0)
        interpolated_data = interpolator(self.x_grid, self.y_grid)
        image = np.ma.masked_where(interpolated_data == 0, interpolated_data)
        return image

    def show(self):
        while not self.axis.has_been_closed:
            t1 = time.process_time()
            while time.process_time() - t1 <= (self.frame_duration):
                continue
            t1 = time.process_time()
            new_batch_data = self.consumer.get_latest_data_packets(self.num_updates, 'default')
            new_image = self.get_image(new_batch_data)
            self.img_axis.set_data(new_image)
            self.fig.canvas.flush_events()
            plt.show()
    

if __name__ == '__main__':

    ###########Only for testing #######################
    class Consumer:
        def __init__(self):
            self.data = np.transpose(np.load('filtered_wet_data.npy'), axes=(1, 0))
            self.pointer = 0

        def get_latest_data_packets(self, bin_length, mode='default'):
            batch_data = self.data[:, self.pointer:self.pointer+bin_length]
            self.pointer += bin_length
            return batch_data

    consumer = Consumer()
    ##################################################
    
    headplot = HeadPlot(consumer, cmap='spring', frame_rate=10)
    headplot.show()