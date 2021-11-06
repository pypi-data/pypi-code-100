import tkinter as tk

from ..abs_class import ThemedWidget
from .frame import Frame


class Entry(tk.Entry, ThemedWidget):
    def __init__(self, master, **kwargs):
        self.border_frame = Frame(master)
        self.border_width = kwargs.get('bd', 1)
        kwargs['bd'] = 0
        kwargs.setdefault('font', 'themed_default')
        ThemedWidget.__init__(self, master, 'entry')
        tk.Entry.__init__(self, self.border_frame, **kwargs)

    def update_theme(self):
        self.border_frame.config(bg=self.get_updated_color('fg', 'main_text'))  # border color
        self.config(bg=self.get_updated_color('bg', 'light_bg'),  # background color
                    fg=self.get_updated_color('fg', 'main_text'),  # font color
                    insertbackground=self.get_updated_color('fg', 'main_text'))  # cursor color

    def pack(self, **kwargs):
        self.border_frame.pack(**kwargs)
        super().pack(padx=self.border_width, pady=self.border_width, ipadx=1, ipady=1, fill=tk.BOTH)


class EntryWithChoices(Entry):
    def __init__(self, master, choices, **kwargs):
        Entry.__init__(self, master, **kwargs)
        self.button = tk.Button(self.border_frame, bd=0, text=" ˅ ")
        self.choices = list(choices)
        self.button.bind("<Button-1>", self.on_click)
        self.sub_window = None

        # implement stretchability
        self.border_frame.grid_rowconfigure(0, weight=1)
        self.border_frame.grid_columnconfigure(0, weight=1)

    @property
    def width(self):
        return self.border_frame.winfo_width()

    @property
    def x(self):
        return self.winfo_rootx() - 1

    @property
    def y_under(self):
        return self.winfo_rooty() + self.winfo_height()

    def update_theme(self):
        super().update_theme()
        self.button.configure(activebackground=self.get_updated_color('bg', 'light_bg'),  # background color
                              background=self.get_updated_color('bg', 'light_bg'),  # background color
                              activeforeground=self.get_updated_color('fg', 'main_text'),  # arrow color
                              foreground=self.get_updated_color('fg', 'main_text'))  # arrow color

    def on_click(self, event):
        self.focus()
        self.sub_window = tk.Toplevel(self.master, bg=self.get_color('light_bg'))
        self.sub_window.overrideredirect(True)
        self.sub_window.geometry(f"{self.width}x300+{self.x}+{self.y_under}")
        self.sub_window.grab_set()
        self.sub_window.grid_rowconfigure(0, weight=1)
        self.sub_window.grid_columnconfigure(0, weight=1)

        listbox = tk.Listbox(self.sub_window, bd=0, highlightthickness=0, font='themed_default',
                             bg=self.get_color('light_bg'), fg=self.get_color('main_text'),
                             selectbackground=self.get_color('primary'))
        scrollbar = tk.Scrollbar(self.sub_window, command=listbox.yview,
                                 highlightcolor="red", troughcolor="yellow", bg="blue")
        listbox['yscrollcommand'] = scrollbar.set

        listbox.grid(padx=(2, 0), pady=(5, 0), row=0, column=0, sticky=tk.NSEW)
        scrollbar.grid(pady=2, row=0, column=1, sticky=tk.NSEW)

        for i, choice in enumerate(self.choices):
            listbox.insert(i, choice)

        listbox.bind('<<ListboxSelect>>', self.choice_selected)

        self.winfo_toplevel().attributes("-disabled", True)

    def choice_selected(self, event):
        selection = event.widget.curselection()
        self.delete(0, tk.END)
        if selection:
            index = selection[0]
            data = self.choices[index]
            self.delete(0, tk.END)
            self.insert(0, data)
        self.winfo_toplevel().attributes("-disabled", False)
        self.sub_window.destroy()

    def pack(self, **kwargs):
        self.border_frame.pack(**kwargs)
        border_x = self.border_width
        if len(self.choices) > 0:
            border_x = (self.border_width, 0)
            self.button.grid(padx=self.border_width, pady=self.border_width, row=0, column=1, sticky=tk.NSEW)
        super().grid(padx=border_x, pady=self.border_width, row=0, column=0, sticky=tk.NSEW)
