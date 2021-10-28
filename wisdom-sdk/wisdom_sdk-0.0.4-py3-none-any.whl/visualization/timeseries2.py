import numpy as np
from vispy import app, scene

class TimePlots:
    def __init__(self, consumer, frame_rate=60, x_axis_size=5, channels=None):

        self.consumer = consumer 
        self.frame_rate = frame_rate

        self.sampling_rate = 976.5625

        num_values_per_plot  = int(self.sampling_rate*x_axis_size)
        self.num_updates = int(self.sampling_rate/frame_rate)

        actual_channel_seq = ['AF3', 'FC3', 'C5', 'C3', 'CP3', 'PO3', 'Fz', 'Cz', 'PO4', 'CP4', 'C4', 'C6', 'FC4', 'AF4', 'CPz', 'Pz']
        if not channels:
            channels = actual_channel_seq
        self.channels = channels

        self.channel_inds = [actual_channel_seq.index(channel) for channel in self.channels]
        self.num_viewboxes = len(self.channels)

        self.viewboxes = []

        for channel_ind, channel in zip(self.channel_inds , self.channels):
            self.viewboxes.append(Viewbox(channel_ind, channel, x_axis_size, num_values_per_plot, self.num_updates))

        self._timer = app.Timer(interval=1/self.frame_rate, connect=self.update_viewboxes, start=True)

    def update_viewboxes(self, event):
        new_data = self.consumer.get_latest_data_packets(self.num_updates, 'default')
        for viewbox in self.viewboxes:
            viewbox.update(new_data[viewbox.channel_ind])

    def show(self):
        self._timer.start()
        app.run()

class Viewbox:
    def __init__(self, channel_ind, channel, x_axis_size, num_values_per_plot, num_updates):

        self.channel_ind = channel_ind
        self.channel = channel
        self.x_axis_size = x_axis_size
        self.num_values_per_plot = num_values_per_plot
        self.num_updates = num_updates
        
        self.data_queue = np.zeros((self.num_values_per_plot))

        self.pos = np.empty((self.num_values_per_plot , 2), dtype=np.float32)
        self.pos[:, 0] = np.linspace(0, self.x_axis_size, self.num_values_per_plot)
        self.pos[:, 1] = np.nan
        
        self.color = np.ones((self.num_values_per_plot, 4), dtype=np.float32)
        self.color[:, 0] = np.linspace(0, 1, self.num_values_per_plot)
        self.color[:, 1] = self.color[::-1, 0]

        self.canvas = scene.SceneCanvas(keys='interactive', title=f"EEG live stream for '{self.channel}'", size=(900, 400), position=(500, 300), show=True)
        self.grid = self.canvas.central_widget.add_grid(spacing=0)

        self.viewbox = self.grid.add_view(row=0, col=1, camera='panzoom')

        self.x_axis = scene.AxisWidget(orientation='bottom')
        self.x_axis.stretch = (1, 0.1)
        self.grid.add_widget(self.x_axis, row=1, col=1)
        self.x_axis.link_view(self.viewbox)
        self.y_axis = scene.AxisWidget(orientation='left')
        self.y_axis.stretch = (0.1, 1)
        self.grid.add_widget(self.y_axis, row=0, col=0)
        self.y_axis.link_view(self.viewbox)

        self.line = scene.Line(self.pos, self.color, parent=self.viewbox.scene)

        self.viewbox.camera.set_range()

    def update(self, new_data):

        self.data_queue[:-self.num_updates] = self.data_queue[self.num_updates:]
        self.data_queue[-self.num_updates:] = new_data
        self.pos[:, 1] = self.data_queue/np.max(np.abs(self.data_queue))
        self.color = np.roll(self.color, 1, axis=0)
        self.line.set_data(pos=self.pos, color=self.color)
        pass

if __name__ == '__main__':

    ###########Only for testing #######################
    class Consumer:
        def __init__(self):
            self.data = np.transpose(np.load('data.npy'), axes=(1, 0))
            self.pointer = 0

        def get_latest_data_packets(self, bin_length, mode='default'):
            batch_data = self.data[:, self.pointer:self.pointer+bin_length]
            self.pointer += bin_length
            return batch_data

    consumer = Consumer()
    ##################################################

    timeplots = TimePlots(consumer, frame_rate=60, x_axis_size=5, channels=['AF3', 'AF4'])
    timeplots.show()