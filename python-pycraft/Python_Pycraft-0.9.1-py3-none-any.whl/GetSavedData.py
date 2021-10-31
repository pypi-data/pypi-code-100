if not __name__ == "__main__":
    print("Started <Pycraft_GetSavedData>")
    class LoadSaveFiles:
        def __init__(self):
            try:
                import os # self mod (module) (module name) (subsection of module) (name references)
                self.mod_OS__ = os
                import sys
                self.mod_Sys__ = sys
                import random
                self.mod_Random__ = random
                import time
                self.mod_Time__ = time
                import timeit
                self.mod_Timeit__ = timeit
                import traceback
                self.mod_Traceback__ = traceback
                import datetime
                self.mod_Datetime__ = datetime
                import json
                self.mod_JSON__ = json
                from tkinter import messagebox
                self.mod_Tkinter_messagebox_ = messagebox
                
                self.base_folder = self.mod_OS__.path.dirname(__file__)
            except Exception as error:
                print(error)
                try:
                    import tkinter as tk
                    root = tk.Tk()
                    root.withdraw()
                    messagebox.showerror("Startup Fail", "Missing required modules")
                    quit()
                except:
                    try:
                        self.mod_Pygame__.quit()
                        sys.exit("0-Thank you for playing")
                    except:
                        quit()
                        
        def ReadMainSave(self):
            with open(self.mod_OS__.path.join(self.base_folder, ("Data_Files\\SaveGameConfig.json")), 'r') as openfile:
                save = self.mod_JSON__.load(openfile)
        
            self.theme = save["theme"]
            self.RunFullStartup = save["startup"]
            self.crash = save["crash"]
            self.Fullscreen = save["WindowStatus"]
            self.FPS = save["FPS"]
            self.aFPS = save["aFPS"]
            self.FOV = save["FOV"]
            self.cameraANGspeed = save["cameraANGspeed"]
            self.RenderFOG = save["RenderFOG"]
            self.aa = save["aa"]
            self.X = save["X"]
            self.Y = save["Y"]
            self.Z = save["Z"]
            self.FanSky = save["FanSky"]
            self.FanPart = save["FanPart"]
            self.sound = save["sound"]
            self.soundVOL = save["soundVOL"]
            self.music = save["music"]
            self.musicVOL = save["musicVOL"]
            self.lastRun = save["lastRun"]
            self.SavedWidth = save["DisplayWidth"]
            self.SavedHeight = save["DisplayHeight"]

        def RepairLostSave(self):
            try:
                SavedData = {"theme":False, "FPS":60, "aFPS":60, "FOV":75, "cameraANGspeed":3, "aa":True, "RenderFOG":True, "FanSky":True, "FanPart":True, "sound":True, "soundVOL":75, "music":True, "musicVOL":50, "X":0, "Y":0, "Z":0, "lastRun":"29/09/2021", 'startup':True, 'crash': False, 'DisplayWidth':1280, 'DisplayHeight':720, 'WindowStatus':False}
                with open(self.mod_OS__.path.join(self.base_folder, ("Data_Files\\SaveGameConfig.json")), 'w') as openfile:
                    self.mod_JSON__.dump(SavedData, openfile)
            except Exception as Message:
                return Message
            else:
                return None

        def SaveTOconfigFILE(self):
            try:
                current_time = self.mod_Datetime__.datetime.now()
                currentDate = f"{current_time.day}/{current_time.month}/{current_time.year}"
                SavedData = {"theme":self.theme, "FPS":self.FPS, "aFPS":self.aFPS, "FOV":self.FOV, "cameraANGspeed":self.cameraANGspeed, "aa":self.aa, "RenderFOG":self.RenderFOG, "FanSky":self.FanSky, "FanPart":self.FanPart, "sound":self.sound, "soundVOL":self.soundVOL, "music":self.music, "musicVOL":self.musicVOL, "X":self.X, "Y":self.Y, "Z":self.Z, "lastRun":currentDate, 'startup':self.RunFullStartup, 'crash': False, 'DisplayWidth':self.SavedWidth, 'DisplayHeight':self.SavedHeight, 'WindowStatus':self.Fullscreen}
                with open(self.mod_OS__.path.join(self.base_folder, ("Data_Files\\SaveGameConfig.json")), 'w') as openfile:
                    self.mod_JSON__.dump(SavedData, openfile)
            except Exception as Message:
                return Message
            else:
                return None
else:
    print("You need to run this as part of Pycraft")
    import tkinter as tk
    from tkinter import messagebox
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Startup Fail", "You need to run this as part of Pycraft, please run the 'main.py' file")
    quit()