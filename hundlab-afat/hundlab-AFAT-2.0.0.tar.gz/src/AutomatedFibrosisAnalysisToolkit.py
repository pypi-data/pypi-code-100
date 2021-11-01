#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn
warnings.filterwarnings('ignore')

if __name__ == "__main__":
    try:
        from AFAT.fibrosis import processAllFiles
        from AFAT.gui import config_run
        import tkinter as tk
        
        #Create main window
        root = tk.Tk()
        root.withdraw()
        gui = config_run.ConfigureRunWidget(root)
        #Run eventloop and create GUI
        root.mainloop()
        root.destroy()
        
        if gui.run_analysis:
            processAllFiles(gui.filepaths, 
                            gui.save_filepath, 
                            gui.save_dirpath,
                            gui.color_rules_filepath)
        else:
            print("Window closed, analysis aborted")
        input('Press Enter to continue ...')
    except Exception as e:
        import traceback
        import sys
        traceback.print_exc(file=sys.stdout)
        print(e)
        input('Press Enter to continue ...')
