import tkinter
import tkinter.messagebox
import tkinter.colorchooser
import tkinter.filedialog

class canvas():
    def __init__(self, title, background_color, canvas_width, canvas_height):
        self.title = title
        self.root = tkinter.Tk()
        self.root.title(title)
        self.canvas = tkinter.Canvas(self.root, bg=background_color, width=canvas_width, height=canvas_height)
        self.canvas.pack()
        self.root.update()
        self.message_box = tkinter.messagebox

    def update(self):
        self.root.update()

    def clear(self):
        self.canvas.delete("all")

    def color_choose(self):
        return tkinter.colorchooser.askcolor(title=self.title)

    def file_choose(self):
        return tkinter.filedialog.askopenfilename()

    def event(self, key, function):
        self.canvas.bind(key, function)