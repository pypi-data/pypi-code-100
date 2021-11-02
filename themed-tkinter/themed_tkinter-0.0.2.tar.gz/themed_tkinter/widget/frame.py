import tkinter as tk

from ..abs_class import ThemedWidget


class Frame(tk.Frame, ThemedWidget):
    def __init__(self, master, **kwargs):
        ThemedWidget.__init__(self, master)
        kwargs = self.update_color_in_kwargs(kwargs)
        tk.Frame.__init__(self, master, **kwargs)

    def update_theme(self):
        self.configure(bg=self.get_updated_color('bg', 'dark_bg'))
        for child in self.children.values():
            if isinstance(child, ThemedWidget):
                child.update_theme()

    def pack(self, fill=tk.X, **kwargs):
        super(Frame, self).pack(fill=fill, **kwargs)
