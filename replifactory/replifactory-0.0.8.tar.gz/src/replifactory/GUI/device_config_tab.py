import ipywidgets as widgets
from IPython.display import clear_output
from ipywidgets import VBox


class DeviceConfigTab:
    def __init__(self, main_gui):
        self.title = "Device config"
        self.main_gui = main_gui
        self.button = widgets.Button(description="Show device parameters")
        self.button.on_click(self.handle_button_click)
        self.output = widgets.Output()
        self.widget = VBox([self.button, self.output])
        self.update()

    def handle_button_click(self, button):
        self.update()

    def update(self):
        if self.main_gui.device is not None:
            with self.output:
                clear_output()
                self.main_gui.device.show_parameters()
