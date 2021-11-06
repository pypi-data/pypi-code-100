import tkinter as tk

from ..abs_class import ThemedWidget
from ..util import color_is_light
from .frame import Frame


class Button(tk.Button, ThemedWidget):
    def __init__(self, master, **kwargs):
        self.border_frame = Frame(master)
        ThemedWidget.__init__(self, master, 'button')
        kwargs = self.update_color_in_kwargs(kwargs)
        self.border_width = kwargs.get('bd', 3)
        kwargs['bd'] = 0
        kwargs.setdefault('font', 'themed_default')
        tk.Button.__init__(self, self.border_frame, **kwargs)
        self.bind("<Button-1>", self.on_button1)
        self.bind("<ButtonRelease>", self.on_button_release)

    def update_theme(self):
        self.border_frame.configure(bg=self.get_color('main_text'))
        self.configure(activebackground=self.border_frame.master.cget('background'),
                       background=self.border_frame.master.cget('background'),

                       activeforeground=self.get_color('primary'),
                       foreground=self.get_color('main_text'))

    def on_button1(self, _):
        self.border_frame.configure(bg=self.get_color('primary'))

    def on_button_release(self, _):
        self.border_frame.configure(bg=self.get_color('main_text'))

    def pack(self, fill=None, **kwargs):
        kwargs['fill'] = fill
        self.border_frame.pack(**kwargs)
        super().pack(padx=self.border_width, pady=self.border_width, ipadx=5, ipady=1, fill=tk.BOTH)


class PrimaryButton(Button):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.text_color = self.get_color('black' if color_is_light(self.get_color('primary')) else 'white')

    def update_theme(self):
        self.text_color = self.get_color('black' if color_is_light(self.get_color('primary')) else 'white')
        self.border_frame.configure(bg=self.get_color('primary'))
        self.configure(activebackground=self.get_color('primary'),
                       background=self.get_color('primary'),

                       activeforeground=self.text_color,
                       foreground=self.text_color)

    def on_button1(self, _):
        self.border_frame.configure(bg=self.text_color)

    def on_button_release(self, _):
        self.border_frame.configure(bg=self.get_color('primary'))


