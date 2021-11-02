import tkinter as tk

from ..abs_class import ThemedWidget


class Label(tk.Label, ThemedWidget):
    def __init__(self, master, **kwargs):
        ThemedWidget.__init__(self, master)
        kwargs = self.update_color_in_kwargs(kwargs)
        kwargs.setdefault('font', 'themed_default')
        tk.Label.__init__(self, master, **kwargs)

    def update_theme(self):
        self.configure(fg=self.get_updated_color('fg', 'main_text'),
                       bg=self.master.cget('bg'))
