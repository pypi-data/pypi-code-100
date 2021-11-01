#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 15:01:40 2021

@author: grat05
"""

def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn
warnings.filterwarnings('ignore')

if __name__ == "__main__":
    try:
        import tkinter as tk
        from AFAT.gui.config_color_rules import ConfigureColorsWidget
        
        root = tk.Tk()
        root.withdraw()
        gui = ConfigureColorsWidget(root)    
        root.mainloop()
        root.destroy()

        input('Press Enter to continue ...')
    except Exception as e:
        import traceback
        import sys
        traceback.print_exc(file=sys.stdout)
        print(e)
        input('Press Enter to continue ...')
