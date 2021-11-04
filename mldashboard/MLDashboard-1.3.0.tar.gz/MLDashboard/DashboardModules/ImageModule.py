from MLDashboard.DashboardModules.Module import Module
from MLDashboard.MLCommunicationBackend import Message
from PIL import Image
from typing import List

def compareImages(imga, imgb):
    if imga == imgb:
        return True

    if list(imga.getdata()) == list(imgb.getdata()):
        return True
    return False

def compareData(itemsa, itemsb, tol):
    for i in range(0, len(itemsa)):
        if abs(itemsa[i] - itemsb[i]) > tol:
            return False
    return True

class ImageModule(Module):
    """Base class for modules that rely on rendering images"""
    def __init__(self, ax, config, title, datarequesttype, reqkeys: List[str] = None):
        basereqkeys = ["width", "height", "rows", "cols", "refreshrate"]
        if reqkeys is not None:
            basereqkeys += reqkeys
        super().__init__(ax, config, title, noticks=True, reqkeys=basereqkeys)

        #defaulting
        if 'conversion' not in self.config:
            self.config['conversion'] = 'L' #grayscale
        if 'cmap' not in self.config:
            self.config['cmap'] = 'gray'

        #storage to quickly swap images
        self.axes = []
        self.axtables = []
        self.text = []
        self.imgs = []
        self.isclear = []

        self.refreshtimer = 0
        self.initreq = False
        self.imgcounter = 0 #index to grab images from
        self.datarequesttype = datarequesttype

        #old ax info
        self.axx = 0
        self.axy = 0
        self.axw = 0
        self.axh = 0

    def shouldRequest(self):
        if not self.initreq:
            self.initreq = True
            return True

        if self.config["refreshrate"] == "once":
            if self.initreq:
                return False
            self.initreq = True
            return True

        if self.config["refreshrate"] <= self.refreshtimer:
            self.refreshtimer = 0
            return True

        self.refreshtimer += 1
        return False

    def generateRequest(self, attempts=None):
        if self.shouldRequest():
            num = self.config['rows'] * self.config['cols']
            d = {"num": num, "startingindex": self.imgcounter, "attempts": attempts}
            self.imgcounter += num
            return [Message(self.datarequesttype, d)]


    def createImages(self, rawdata):
        images = []
        for image in rawdata:
            image = image.reshape(self.config['width'],self.config['height'])
            img = Image.fromarray(image * 255)
            images.append(img.convert(self.config['conversion']))
        return images

    def updateImageGrid(self, imgs = None, text = None, color=None):
        """Will not rerender unless it is necessary."""
        if imgs is None:
            imgs = self.imgs
        if text is None:
            text = self.text
        if color is None:
            color = ['black'] * len(text)

        if len(imgs) > 0:
            b = self.ax.get_position()
            x = b.x0
            y = b.y0
            width = b.width
            height = b.height

            rerender = not compareData([x, y, width, height], [self.axx, self.axy, self.axw, self.axh], 0.01)
            self.axx = x
            self.axy = y
            self.axw = width
            self.axh = height

            rows = self.config['rows']
            cols = self.config['cols']

            imgwidth = (width / cols)
            imgheight = (height / rows)

            counter = 0
            ypos = y
            for row in range(0, rows):
                xpos = x
                for col in range(0, cols):
                    xcoord = xpos + imgwidth / 6
                    ycoord = ypos + imgheight / 8
                    truewidth = imgwidth / 1.5
                    trueheight = imgheight / 1.5

                    if counter >= len(self.axes):
                        if counter < len(imgs):
                            ax, table = self.displayImage(xcoord, ycoord, truewidth, trueheight,
                                                               imgs[counter], text[counter], color[counter])
                            self.axes.append(ax)
                            self.axtables.append(table)
                            self.isclear.append(False)
                    else:
                        if rerender:
                            self.axes[counter].set_position((xcoord, ycoord, truewidth, trueheight))

                        if counter < len(imgs):
                            if counter >= len(self.text) or text[counter] != self.text[counter]:
                                t = self.axtables[counter][0,0].get_text()
                                t.set_text(text[counter])
                                t.set_color(color[counter])
                                t.set_fontsize(12) #this gets auto scaled down
                            if counter >= len(self.imgs) or not compareImages(imgs[counter], self.imgs[counter]):
                                self.axes[counter].imshow(imgs[counter], cmap=self.config['cmap'])
                                self.isclear[counter] = False
                                self.axes[counter].axis('on')
                        else:
                            if not self.isclear[counter]:
                                self.axes[counter].clear()
                                self.isclear[counter] = True
                                self.axes[counter].axis('off')

                    counter += 1
                    xpos += imgwidth
                ypos += imgheight

        self.imgs = imgs
        self.text = text


    def displayImage(self, x, y, width, height, img, text, textcolor='black'):
        #imshow will only shrink and resize axes
        fig = self.ax.get_figure()
        ax = fig.add_axes((x, y, width, height))
        ax.imshow(img, cmap=self.config['cmap'])
        ax.tick_params(axis='both', which='both', bottom=False, top=False,
                                labelbottom=False, right=False, left=False, labelleft=False)

        table = ax.table([[text]], loc='top', colWidths=[1.4], cellLoc='center')
        table[0,0].get_text().set_color(textcolor)
        table[0, 0].set_height(0.2)
        table[0,0].get_text().set_fontsize(12)  # this gets auto scaled down
        table[0,0].set_linewidth(0)
        return ax, table