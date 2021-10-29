import wx
from .PyParams import Wolf_Param

if __name__=="__main__":
    ex = wx.App()
    frame = Wolf_Param(None,"Params")
    ex.MainLoop()