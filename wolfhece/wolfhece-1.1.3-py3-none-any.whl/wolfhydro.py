from os import path
import sys
import wx
from wolfhece.PyGui import HydrologyModel

def main(strmydir=''):
    ex = wx.App()
    mydro=HydrologyModel()
    ex.MainLoop()

if __name__=='__main__':
    main()