
import numpy as np
from vispy import gloo, app

class TimePlot(app.Canvas):

    def __init__(self, consumer, channels=None, frame_rate=60, x_axis_size=3, uniform_scale=True, num_plot_columns=1):

        app.Canvas.__init__(self, title='EEG live stream', keys='interactive')

        self.consumer = consumer 
        self.uniform_scale = uniform_scale

        actual_channel_sequence = ['AF3', 'FC3', 'C5', 'C3', 'CP3', 'PO3', 'Fz', 'Cz', 'PO4', 'CP4', 'C4', 'C6', 'FC4', 'AF4', 'CPz', 'Pz']

        if not channels:
            self.channels = actual_channel_sequence
        else:
            self.channels = channels

        self.sampling_rate = 976.5625
        self.screen_size = (1300, 900)
        self.frame_rate = frame_rate
        self.x_axis_size = x_axis_size
        self.num_plot_columns = num_plot_columns

        self.channel_inds = [actual_channel_sequence.index(channel) for channel in self.channels]
        self.num_plots = len(self.channels)

        self.num_plot_rows = int(self.num_plots/self.num_plot_columns)

        self.num_values_per_plot = int(self.x_axis_size*self.sampling_rate)

        self.num_updates = int(self.sampling_rate/self.frame_rate)

        self.plot_data = np.zeros((self.num_plots, self.num_values_per_plot)).astype(np.float32)

        self.color = np.repeat(np.random.uniform(size=(self.num_plots, 3), low=.5, high=.9), 
                        self.num_values_per_plot, axis=0).astype(np.float32)

        self.index = np.c_[np.repeat(np.repeat(np.arange(self.num_plot_columns), self.num_plot_rows), self.num_values_per_plot),
                                np.repeat(np.tile(np.arange(self.num_plot_rows), self.num_plot_columns), self.num_values_per_plot),
                                np.tile(np.arange(self.num_values_per_plot), self.num_plots)].astype(np.float32)

        
        self.program = gloo.Program(vert_shader(), frag_shader())
        self.program['a_position'] = self.plot_data.reshape(-1, 1)
        self.program['a_color'] = self.color
        self.program['a_index'] = self.index
        self.program['u_scale'] = (1., 1.)
        self.program['u_size'] = (self.num_plot_rows, self.num_plot_columns)
        self.program['u_n'] = self.num_values_per_plot
        self.program['u_yscale'] = 1

        gloo.set_viewport(0, 0, *self.physical_size)

        self._timer = app.Timer(interval=1/self.frame_rate, connect=self.on_timer, start=True)

        gloo.set_state(clear_color='black', blend=True,
                       blend_func=('src_alpha', 'one_minus_src_alpha'))

    def on_resize(self, event):
        gloo.set_viewport(0, 0, *event.physical_size)

    def on_mouse_wheel(self, event):
        dx = np.sign(event.delta[1]) * .05
        scale_x, scale_y = self.program['u_scale']
        scale_x_new, scale_y_new = (scale_x * np.exp(2.5*dx),
                                    scale_y * np.exp(0.0*dx))
        self.program['u_scale'] = (max(1, scale_x_new), max(1, scale_y_new))
        self.update()

    def on_timer(self, event):

        self.plot_data[:, :-self.num_updates] = self.plot_data[:, self.num_updates:]
        self.plot_data[:, -self.num_updates:] = self.consumer.get_latest_data_packets(self.num_updates, 'default')[self.channel_inds]

        if not self.uniform_scale:
            plot_data_updated = (self.plot_data/np.max(np.abs(self.plot_data), axis=1).reshape(-1,1)).ravel()
        else:
            plot_data_updated = (self.plot_data/np.max(np.abs(self.plot_data)).reshape(-1,1)).ravel()

        self.program['a_position'].set_data(plot_data_updated)

        self.update()

    def on_draw(self, event):
        gloo.clear()
        self.program.draw('line_strip')

    def show_plot(self):
        self.show()
        app.run()

def vert_shader():
    VERT_SHADER = """
    #version 120
    // y coordinate of the position.
    attribute float a_position;
    // row, col, and time index.
    attribute vec3 a_index;
    varying vec3 v_index;
    // 2D scaling factor (zooming).
    uniform vec2 u_scale;
    // Size of the table.
    uniform vec2 u_size;
    // Number of samples per signal.
    uniform float u_n;
    // Color.
    attribute vec3 a_color;
    varying vec4 v_color;
    // Varying variables used for clipping in the fragment shader.
    varying vec2 v_position;
    varying vec4 v_ab;
    uniform float u_yscale;
    void main() {
        float nrows = u_size.x;
        float ncols = u_size.y;
        // Compute the x coordinate from the time index.
        float x = -1 + 2*a_index.z / (u_n-1);
        vec2 position = vec2(x - (1 - 1 / u_scale.x), a_position / u_yscale);
        // Find the affine transformation for the subplots.
        vec2 a = vec2(1./ncols, 1./nrows)*.9;
        vec2 b = vec2(-1 + 2*(a_index.x+.5) / ncols,
                    -1 + 2*(a_index.y+.5) / nrows);
        // Apply the static subplot transformation + scaling.
        gl_Position = vec4(a*u_scale*position+b, 0.0, 1.0);
        v_color = vec4(a_color, 1.);
        v_index = a_index;
        // For clipping test in the fragment shader.
        v_position = gl_Position.xy;
        v_ab = vec4(a, b);
    }
    """
    return VERT_SHADER

def frag_shader():
    FRAG_SHADER = """
    #version 120
    varying vec4 v_color;
    varying vec3 v_index;
    varying vec2 v_position;
    varying vec4 v_ab;
    void main() {
        gl_FragColor = v_color;
        // Discard the fragments between the signals (emulate glMultiDrawArrays).
        if ((fract(v_index.x) > 0.) || (fract(v_index.y) > 0.))
            discard;
        // Clipping test.
        vec2 test = abs((v_position.xy-v_ab.zw)/v_ab.xy);
        if ((test.x > 1) || (test.y > 1))
            discard;
    }
    """
    return FRAG_SHADER

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
    
    timeplot = TimePlot(consumer, channels=None, frame_rate=60, x_axis_size=3, uniform_scale=True, num_plot_columns=1)
    timeplot.show_plot()