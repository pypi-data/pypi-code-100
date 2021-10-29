from os import path
import sys
import wx
from wolfhece.PyGui import HydrologyModel

def main(strmydir=''):
    if strmydir!='':
        print(strmydir)
        mydir=path.normpath(strmydir)
        print(mydir)

        ex = wx.App()
        mydro=HydrologyModel(mydir)
        ex.MainLoop()
    else:
        print('You must define the root directory of the model ! -- Retry !')
        print('python3 -m wolfhydro.py "mydir"')
        print('')
        print('If you pass a Windows Path, use raw string (with "r" before) r\'mypath\'')

if __name__=='__main__':
    if len(sys.argv)>1:
        main(sys.argv[1:])
    else:
        main()