import wx
from .PyDraw import WolfMapViewer

class GuiHydrology(WolfMapViewer):

    def __init__(self, parent, title,w=500,h=500):
        super(GuiHydrology, self).__init__(parent, title = title,w=w,h=h)

        parametersmenu = wx.Menu()
        paramgen = parametersmenu.Append(1000,'Main model','General parameters')
        paramgen = parametersmenu.Append(1001,'Basin','Basin parameters')
        self.menubar.Append(parametersmenu,'&Parameters')

        toolsmenu = wx.Menu()
        newtool = toolsmenu.Append(wx.ID_EXECUTE,'New tool','My new tool...')
        self.menubar.Append(toolsmenu,'&Tools')

    
    def OnMenubar(self,event):

        super().OnMenubar(event)

        id = event.GetId()
        item = self.menubar.FindItemById(id)

        if id==wx.ID_EXECUTE :
            print('Do anything !!')
        if id==1000 :
            self.Parent.mainparams.Show()
        if id==1001 :
            self.Parent.basinparams.Show()


