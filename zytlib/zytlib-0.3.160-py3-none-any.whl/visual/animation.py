from matplotlib import pyplot as plt
from ..vector import vector
from ..table import table

class animation_content:

    def __init__(self, ax, max_frame):
        self.ax = ax
        self.max_frame = max_frame
        self.default_colors = [u'b', u'g', u'r', u'c', u'm', u'y', u'k']

    def init(self):
        raise NotImplementedError()

    def update_frame(self, frame):
        raise NotImplementedError()

class TimeStamp(animation_content):

    def __init__(self, ax, max_frame):
        super().__init__(ax, max_frame)
        self.curves = vector()

    def register(self, content, **kwargs):
        assert isinstance(content, list)
        content = vector(content)
        assert content.length >= self.max_frame
        content = content[:self.max_frame]
        curve = table(content=content, color=self.default_colors[len(self.curves)], linewidth=1, label=None)
        curve.update_exist(kwargs)
        self.curves.append(curve)

    def init(self):
        self.N = len(self.curves)
        lines = vector()
        for index, curve in enumerate(self.curves):
            ln, = self.ax.plot(range(self.max_frame), curve["content"], color=curve["color"], linewidth=curve["linewidth"], label=None)
            lines.append(ln)
        self.ax.legend()
        self.dots = self.ax.scatter(vector.zeros(self.N), self.curves.map(lambda x: x["content"][0]), color=self.curves.map(lambda x: x["color"]))
        return tuple(lines.append(self.dots))

    def update_frame(self, frame):
        self.dots.set_offsets(vector.zip(vector.constant_vector(frame, self.N), self.curves.map(lambda x: x["content"][frame])))
        return tuple([self.dots])
