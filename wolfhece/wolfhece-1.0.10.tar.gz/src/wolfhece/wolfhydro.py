from os import path
import sys
import wx
from .PyGui import HydrologyModel

if __name__=='__main__':
    if len(sys.argv)==2:
        print(sys.argv[1])
        print(path.normpath(sys.argv[1]))

        ex = wx.App()
        mydir=path.normpath(sys.argv[1])
        mydro=HydrologyModel(mydir)
        ex.MainLoop()
    else:
        print('You must define the root directory of the model ! -- Retry !')
        print('python3 -m wolfhydro.py "mydir"')