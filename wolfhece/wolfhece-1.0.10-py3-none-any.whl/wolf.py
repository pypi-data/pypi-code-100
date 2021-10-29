from os import path
import sys
import wx
from .PyGui import MapManager

if __name__=='__main__':
    ex = wx.App()
    mydro=MapManager()
    ex.MainLoop()
