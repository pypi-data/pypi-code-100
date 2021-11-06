import tkinter as tk
from ..abs_class import ThemedWindow


class TopLevel(tk.Toplevel, ThemedWindow):
    def __init__(self, master, **kw):
        tk.Toplevel.__init__(self, master, **kw)
        ThemedWindow.__init__(self)
        # Switch focus to this window
        self.focus()
        # Disable the calling window until we are done
        # `grab_release()` isn't necessary. Control is automatically released when toplevels are closed
        self.grab_set()
        self.after(10, self.__move_to_center_of_parent_win)

    def __move_to_center_of_parent_win(self):
        self.update_idletasks()
        # We use double slash '//' to make a integer division
        x = self.master.winfo_x() + (self.master.winfo_width() - self.width) // 2
        y = self.master.winfo_y() + (self.master.winfo_height() - self.height) // 2
        self.geometry(f"{self.winfo_width()}x{self.winfo_height()}+{x}+{y}")

    @property
    def theme(self):
        return self.master.theme
