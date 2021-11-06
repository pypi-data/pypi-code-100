import tkinter as tk

from ..abs_class import ThemedWidget
from .frame import Frame


class Text(tk.Text, ThemedWidget):
    def __init__(self, master, **kwargs):
        self.border_frame = Frame(master)
        ThemedWidget.__init__(self, master)
        kwargs = self.update_color_in_kwargs(kwargs)
        self.border_width = kwargs.get('bd', 1)
        kwargs['bd'] = 0
        kwargs.setdefault('font', 'themed_default')
        tk.Text.__init__(self, self.border_frame, **kwargs)

    def update_theme(self):
        self.border_frame.configure(bg=self.get_updated_color('fg', 'main_text'))  # border color
        self.configure(bg=self.get_updated_color('bg', 'light_bg'),  # background color
                       fg=self.get_updated_color('fg', 'main_text'),  # font color
                       insertbackground=self.get_updated_color('fg', 'main_text'))  # cursor color

    def pack(self, expand=True, fill=tk.BOTH, **kwargs):
        self.border_frame.pack(expand=expand, fill=fill, **kwargs)
        super().pack(padx=self.border_width, pady=self.border_width, ipadx=5, ipady=1, fill=tk.BOTH)


class ScrollableText(tk.Frame, ThemedWidget):
    def __init__(self, master, **kwargs):
        ThemedWidget.__init__(self, master, 'frame')
        kwargs['bd'] = 1
        tk.Frame.__init__(self, master, **kwargs)

        # ensure a consistent GUI size
        self.grid_propagate(False)

        # implement stretchability
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.text = tk.Text(self, bd=0, font='themed_default')
        self.scrollbar = tk.Scrollbar(self, command=self.text.yview)
        self.text['yscrollcommand'] = self.scrollbar.set

        self.text.grid(row=0, column=0, sticky=tk.NSEW)
        self.scrollbar.grid(row=0, column=1, sticky=tk.NSEW)

    def update_theme(self):
        self.text.configure(bg=self.get_updated_color('bg', 'light_bg'),  # background color
                            fg=self.get_updated_color('fg', 'main_text'),  # font color
                            insertbackground=self.get_updated_color('fg', 'main_text'))  # cursor color
