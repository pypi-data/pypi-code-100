if not __name__ == "__main__":
    print("Started <Pycraft_TkinterUtils>")
    class TkinterInfo:
        def __init__(self):
            try:
                import tkinter as tk
                self.mod_Tkinter__tk = tk # [self] mod (module) (module name) (subsection of module) (name references)
                import tkinter.ttk # Class _ <class_name> _ variables
                self.mod_Tkinter_ttk_ = tkinter.ttk
                from tkinter import messagebox
                self.mod_Tkinter_messagebox_ = messagebox
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
                        self.mod_Sys__.exit("0.0 -Thank you for playing")
                    except:
                        quit()

        def CreateTkinterWindow(self):
            DataWindow = self.mod_Tkinter__tk.Tk()
            DataWindow.title("Player Information")
            DataWindow.configure(width = 500, height = 300) 
            DataWindow.configure(bg="lightblue") 
            VersionData = f"Pycraft: v{self.version}"
            CoordinatesData = f"Coordinates: x: {self.X} y: {self.Y} z: {self.Z} Facing: 0.0, 0.0, 0.0" 
            FPSData = f"FPS: Actual: {self.eFPS} Max: {self.FPS}" 
            VersionData = self.mod_Tkinter__tk.Label(DataWindow, text=VersionData) 
            CoordinatesData = self.mod_Tkinter__tk.Label(DataWindow, text=CoordinatesData) 
            FPSData = self.mod_Tkinter__tk.Label(DataWindow, text=FPSData) 
            VersionData.grid(row = 0, column = 0, columnspan = 2) 
            CoordinatesData.grid(row = 1, column = 0, columnspan = 2)
            FPSData.grid(row = 2, column = 0, columnspan = 2)
            DataWindow.mainloop() 
            DataWindow.quit()
else:
    print("You need to run this as part of Pycraft")
    import tkinter as tk
    from tkinter import messagebox
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Startup Fail", "You need to run this as part of Pycraft, please run the 'main.py' file")
    quit()