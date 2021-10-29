from os import path
import sys
import wx
from wolfhece.PyGui import MapManager
import wolfhydro
#from wolfhece.wolfresults_2D import *

def main():
    ex = wx.App()
    mydro=MapManager()
    ex.MainLoop()

if __name__=='__main__':
    main()