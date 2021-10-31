import matplotlib.pyplot as plt


class Doxyplot:
    """Class for automated plotting of xy-scatter data"""
    def __init__(self):
        self.x_list = []
        self.y_list = []
        self.c_list = []
        self.label_list = []
        self.linewidth = []
        pass

    def append_data(self, x, y, c, label, linewidth=2.0):
        self.x_list.append(x)
        self.y_list.append(y)
        self.c_list.append(c)
        self.label_list.append(label)
        self.linewidth.append(linewidth)

    def construct_plot(self,title,xlabel,ylabel,save=False,xymin=False,xymax=False,figsize=(7, 5)):
        fig = plt.figure(figsize=figsize)
        ax1 = fig.add_subplot(111)
        ax1.set_title(title)
        ax1.set_xlabel(xlabel)
        ax1.set_ylabel(ylabel)
        for i in range(len(self.x_list)):
            ax1.plot(self.x_list[i],self.y_list[i],c=self.c_list[i],label=self.label_list[i],linewidth=self.linewidth[i])
        leg = ax1.legend()
        if xymin:
            ax1.set_xlim(xmin=xymin[0])
            ax1.set_ylim(ymin=xymin[1])
        if xymax:
            ax1.set_xlim(xmax=xymax[0])
            ax1.set_ylim(ymax=xymax[1])
        if save:
            fig.savefig(save, format="png",
                        dpi=200, bbox_inches="tight")
        return (ax1, fig)

