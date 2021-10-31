if not __name__ == "__main__":
    print("Started <Pycraft_GetWorldCollisions>")
    class GetMapCollisions:
        def __init__(self):
            try:
                import os
                self.mod_OS__ = os
                import sys
                self.mod_Sys__ = sys
                from tkinter import messagebox
                self.mod_Tkinter_messagebox_ = messagebox
                import numpy
                self.mod_Numpy__ = numpy
                import array
                self.mod_Array__ = array
                
                self.base_folder = os.path.dirname(__file__)
            except Exception as error:
                print(error)
                try:
                    import tkinter as tk
                    root = tk.Tk()
                    root.withdraw()
                    self.mod_Tkinter_messagebox_.showerror("Startup Fail", "Missing required modules")
                    quit()
                except:
                    try:
                        self.mod_Pygame__.quit()
                        sys.exit("Thank you for playing")
                    except:
                        quit()

        def GetCollisions(self):
            for i in range(len(self.Map_collisions)):
                if int(self.Map_collisions[i][0]*self.G3Dscale) <= int(self.X-1) or int(self.Map_collisions[i][0]*self.G3Dscale) >= int(self.X+1):
                    if int(self.Map_collisions[i][2]*self.G3Dscale) <= int(self.Z-1) or int(self.Map_collisions[i][2]*self.G3Dscale) >= int(self.Z+1):
                        arr = [True, self.Map_collisions[i][1]]
                        return arr
                    else:
                        arr = ["Partial Detection Found",0]
                        return arr
                else:
                    arr = [False, 0]
                    return arr
else:
    print("You need to run this as part of Pycraft")
    import tkinter as tk
    from tkinter import messagebox
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Startup Fail", "You need to run this as part of Pycraft, please run the 'main.py' file")
    quit()