from tkinter import Canvas
import tkinter as tk

OBJECT_TYPE_NONE = 0
OBJECT_TYPE_IMAGE = 1
OBJECT_TYPE_STATUS = 2


class OOCanvas(Canvas):
    def __init__(self, master=None, image=None, command=None, **kw):
        super(OOCanvas, self).__init__(
            master=master, image=image, command=command, **kw)
        self.items_list = list()

    def create_ooImage(self):
        img = OOCanvasImage(self)
        self.items_list.append(img)

    def create_ooStatus(self, x=0, y=0):
        st = OOCanvasStatus(self, x, y)
        self.items_list.append(st)
        return st


class OOCanvasItem:
    def __init__(self, canvas, x, y):
        self.canv = canvas
        self.objectType = OBJECT_TYPE_NONE

    def set_location(self, x, y):
        raise NotImplementedError("Please Implement this method")

    def move(self, xmovement, ymovement):
        raise NotImplementedError("Please Implement this method")

    def raise_to_top(self):
        raise NotImplementedError("Please Implement this method")


class OOCanvasSimpleItem(OOCanvasItem):
    def __init__(self, canvas, x, y):
        super(OOCanvasSimpleItem, self).__init__(canvas, x=x, y=y)
        self.id = None

    def set_location(self, x, y):
        self.canv.moveto(self.id, x, y)
        return self

    def move(self, xmovement, ymovement):
        self.canv.move(self.id, xmovement, ymovement)
        return self

    def raise_to_top(self):
        self.canv.tag_raise(self.id)
        return self


class OOCanvasComplexItem(OOCanvasItem):
    def __init__(self, canvas, x, y):
        super(OOCanvasComplexItem, self).__init__(canvas, x=x, y=y)
        self.ids = list()

    def set_location(self, x, y):
        pass

    def move(self, xmovement, ymovement):
        pass

    def raise_to_top(self):
        pass

# region potential
    # def addtag_above(self, newtag):
    #     """Add tag NEWTAG to all items above TAGORID."""
    #     self.canvas.addtag_above(newtag, self.canvasItemId)

    # def addtag_all(self, newtag):
    #     """Add tag NEWTAG to all items."""
    #     self.canvas.addtag_all(newtag, self.canvasItemId)

    # def addtag_below(self, newtag):
    #     """Add tag NEWTAG to all items below TAGORID."""
    #     self.canvas.addtag_below(newtag, self.canvasItemId)

    # def addtag_closest(self, newtag, x, y, halo=None, start=None):
    #     """Add tag NEWTAG to item which is closest to pixel at X, Y.
    #     If several match take the top-most.
    #     All items closer than HALO are considered overlapping (all are
    #     closests). If START is specified the next below this tag is taken."""
    #     self.canvas.addtag_closest(self, newtag, x, y, halo=halo, start=start)

    # def addtag_enclosed(self, newtag, x1, y1, x2, y2):
    #     """Add tag NEWTAG to all items in the rectangle defined
    #     by X1,Y1,X2,Y2."""
    #     self.addtag(newtag, 'enclosed', x1, y1, x2, y2)

    # def addtag_overlapping(self, newtag, x1, y1, x2, y2):
    #     """Add tag NEWTAG to all items which overlap the rectangle
    #     defined by X1,Y1,X2,Y2."""
    #     self.addtag(newtag, 'overlapping', x1, y1, x2, y2)

    # def addtag_withtag(self, newtag, tagOrId):
    #     """Add tag NEWTAG to all items with TAGORID."""
    #     self.addtag(newtag, 'withtag', tagOrId)

    # def bbox(self, *args):
    #     """Return a tuple of X1,Y1,X2,Y2 coordinates for a rectangle
    #     which encloses all items with tags specified as arguments."""
    #     return self._getints(
    #         self.tk.call((self._w, 'bbox') + args)) or None

    # def tag_unbind(self, tagOrId, sequence, funcid=None):
    #     """Unbind for all items with TAGORID for event SEQUENCE  the
    #     function identified with FUNCID."""
    #     self.tk.call(self._w, 'bind', tagOrId, sequence, '')
    #     if funcid:
    #         self.deletecommand(funcid)

    # def tag_bind(self, tagOrId, sequence=None, func=None, add=None):
    #     """Bind to all items with TAGORID at event SEQUENCE a call to function FUNC.

    #     An additional boolean parameter ADD specifies whether FUNC will be
    #     called additionally to the other bound function or whether it will
    #     replace the previous function. See bind for the return value."""
    #     return self._bind((self._w, 'bind', tagOrId),
    #                       sequence, func, add)

    # def canvasx(self, screenx, gridspacing=None):
    #     """Return the canvas x coordinate of pixel position SCREENX rounded
    #     to nearest multiple of GRIDSPACING units."""
    #     return self.tk.getdouble(self.tk.call(
    #         self._w, 'canvasx', screenx, gridspacing))

    # def canvasy(self, screeny, gridspacing=None):
    #     """Return the canvas y coordinate of pixel position SCREENY rounded
    #     to nearest multiple of GRIDSPACING units."""
    #     return self.tk.getdouble(self.tk.call(
    #         self._w, 'canvasy', screeny, gridspacing))

    # def coords(self, *args):
    #     """Return a list of coordinates for the item given in ARGS."""
    #     # XXX Should use _flatten on args
    #     return [self.tk.getdouble(x) for x in
    #             self.tk.splitlist(
    #         self.tk.call((self._w, 'coords') + args))]

    # def dchars(self, *args):
    #     """Delete characters of text items identified by tag or id in ARGS (possibly
    #     several times) from FIRST to LAST character (including)."""
    #     self.tk.call((self._w, 'dchars') + args)

    # def delete(self, *args):
    #     """Delete items identified by all tag or ids contained in ARGS."""
    #     self.tk.call((self._w, 'delete') + args)

    # def dtag(self, *args):
    #     """Delete tag or id given as last arguments in ARGS from items
    #     identified by first argument in ARGS."""
    #     self.tk.call((self._w, 'dtag') + args)

    # def find(self, *args):
    #     """Internal function."""
    #     return self._getints(
    #         self.tk.call((self._w, 'find') + args)) or ()

    # def find_above(self, tagOrId):
    #     """Return items above TAGORID."""
    #     return self.find('above', tagOrId)

    # def find_all(self):
    #     """Return all items."""
    #     return self.find('all')

    # def find_below(self, tagOrId):
    #     """Return all items below TAGORID."""
    #     return self.find('below', tagOrId)

    # def find_closest(self, x, y, halo=None, start=None):
    #     """Return item which is closest to pixel at X, Y.
    #     If several match take the top-most.
    #     All items closer than HALO are considered overlapping (all are
    #     closest). If START is specified the next below this tag is taken."""
    #     return self.find('closest', x, y, halo, start)

    # def find_enclosed(self, x1, y1, x2, y2):
    #     """Return all items in rectangle defined
    #     by X1,Y1,X2,Y2."""
    #     return self.find('enclosed', x1, y1, x2, y2)

    # def find_overlapping(self, x1, y1, x2, y2):
    #     """Return all items which overlap the rectangle
    #     defined by X1,Y1,X2,Y2."""
    #     return self.find('overlapping', x1, y1, x2, y2)

    # def find_withtag(self, tagOrId):
    #     """Return all items with TAGORID."""
    #     return self.find('withtag', tagOrId)

    # def focus(self, *args):
    #     """Set focus to the first item specified in ARGS."""
    #     return self.tk.call((self._w, 'focus') + args)

    # def gettags(self, *args):
    #     """Return tags associated with the first item specified in ARGS."""
    #     return self.tk.splitlist(
    #         self.tk.call((self._w, 'gettags') + args))

    # def icursor(self, *args):
    #     """Set cursor at position POS in the item identified by TAGORID.
    #     In ARGS TAGORID must be first."""
    #     self.tk.call((self._w, 'icursor') + args)

    # def index(self, *args):
    #     """Return position of cursor as integer in item specified in ARGS."""
    #     return self.tk.getint(self.tk.call((self._w, 'index') + args))

    # def insert(self, *args):
    #     """Insert TEXT in item TAGORID at position POS. ARGS must
    #     be TAGORID POS TEXT."""
    #     self.tk.call((self._w, 'insert') + args)

    # def itemcget(self, tagOrId, option):
    #     """Return the resource value for an OPTION for item TAGORID."""
    #     return self.tk.call(
    #         (self._w, 'itemcget') + (tagOrId, '-'+option))

    # def itemconfigure(self, tagOrId, cnf=None, **kw):
    #     """Configure resources of an item TAGORID.

    #     The values for resources are specified as keyword
    #     arguments. To get an overview about
    #     the allowed keyword arguments call the method without arguments.
    #     """
    #     return self._configure(('itemconfigure', tagOrId), cnf, kw)

    # itemconfig = itemconfigure

    # # lower, tkraise/lift hide Misc.lower, Misc.tkraise/lift,
    # # so the preferred name for them is tag_lower, tag_raise
    # # (similar to tag_bind, and similar to the Text widget);
    # # unfortunately can't delete the old ones yet (maybe in 1.6)
    # def tag_lower(self, *args):
    #     """Lower an item TAGORID given in ARGS
    #     (optional below another item)."""
    #     self.tk.call((self._w, 'lower') + args)

    # lower = tag_lower

    # def postscript(self, cnf={}, **kw):
    #     """Print the contents of the canvas to a postscript
    #     file. Valid options: colormap, colormode, file, fontmap,
    #     height, pageanchor, pageheight, pagewidth, pagex, pagey,
    #     rotate, width, x, y."""
    #     return self.tk.call((self._w, 'postscript') +
    #                         self._options(cnf, kw))

    # def tag_raise(self, *args):
    #     """Raise an item TAGORID given in ARGS
    #     (optional above another item)."""
    #     self.tk.call((self._w, 'raise') + args)

    # lift = tkraise = tag_raise

    # def scale(self, *args):
    #     """Scale item TAGORID with XORIGIN, YORIGIN, XSCALE, YSCALE."""
    #     self.tk.call((self._w, 'scale') + args)

    # def scan_mark(self, x, y):
    #     """Remember the current X, Y coordinates."""
    #     self.tk.call(self._w, 'scan', 'mark', x, y)

    # def scan_dragto(self, x, y, gain=10):
    #     """Adjust the view of the canvas to GAIN times the
    #     difference between X and Y and the coordinates given in
    #     scan_mark."""
    #     self.tk.call(self._w, 'scan', 'dragto', x, y, gain)

    # def select_adjust(self, tagOrId, index):
    #     """Adjust the end of the selection near the cursor of an item TAGORID to index."""
    #     self.tk.call(self._w, 'select', 'adjust', tagOrId, index)

    # def select_clear(self):
    #     """Clear the selection if it is in this widget."""
    #     self.tk.call(self._w, 'select', 'clear')

    # def select_from(self, tagOrId, index):
    #     """Set the fixed end of a selection in item TAGORID to INDEX."""
    #     self.tk.call(self._w, 'select', 'from', tagOrId, index)

    # def select_item(self):
    #     """Return the item which has the selection."""
    #     return self.tk.call(self._w, 'select', 'item') or None

    # def select_to(self, tagOrId, index):
    #     """Set the variable end of a selection in item TAGORID to INDEX."""
    #     self.tk.call(self._w, 'select', 'to', tagOrId, index)

    # def type(self, tagOrId):
    #     """Return the type of the item TAGORID."""
    #     return self.tk.call(self._w, 'type', tagOrId) or None
# endregion


class OOCanvasImage(OOCanvasSimpleItem):
    def __init__(self, canvas, x, y):
        super(OOCanvasImage, self).__init__(canvas, x=x, y=y)
        self.objectType = OBJECT_TYPE_IMAGE

    def set_image(self, image):
        self.canv.itemconfig(self.id, image=image)


class OOCanvasStatus(OOCanvasSimpleItem):
    def __init__(self, canvas, x, y):
        super(OOCanvasStatus, self).__init__(canvas, x=x, y=y)
        self.objectType = OBJECT_TYPE_STATUS
        self.id = self.canv.create_image(x, y)
        self.statuses = dict()
        self.__loop_active = False
        self.__loop = None
        self.__frames = None
        self.__frames_len = 0
        self.__current_frame_index = 1
        self.__nextFrameAfter_ms = 0

    def set_status(self, statusKey, image, framesArray=None, nextFrameAfter_ms=500):
        self.statuses[statusKey] = {
            'image': image, 'framesArray': framesArray, 'nextFrameAfter_ms': nextFrameAfter_ms}
        return self

    def select_status(self, statusKey):
        st = self.statuses.get(statusKey)
        if st == None:
            self.canv.itemconfig(self.id, image=None)
        else:
            if self.__loop_active:
                self.__loop_active = False
                self.canv.master.after_cancel(self.__loop)
            self.canv.itemconfig(self.id, image=st['image'])
            self.canv.tag_raise(self.id)
            if st['framesArray'] is not None:
                self.__frames = st['framesArray']
                self.__frames_len = len(self.__frames)
                self.__current_frame_index = 0
                self.__nextFrameAfter_ms = st['nextFrameAfter_ms']
                self.__loop_active = True
                self.__loop = self.canv.master.after(
                    st['nextFrameAfter_ms'], self.__frame_manager)
        return self

    def __frame_manager(self):
        self.canv.itemconfig(
            self.id, image=self.__frames[self.__current_frame_index])
        if self.__current_frame_index >= self.__frames_len-1:
            self.__current_frame_index = 0
        else:
            self.__current_frame_index += 1
        self.__loop = self.canv.master.after(
            self.__nextFrameAfter_ms, self.__frame_manager)
