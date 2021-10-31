if not __name__ == "__main__":
    print("Started <Pycraft_CaptionUtils>")
    class GenerateCaptions:
        def __init__(self):
            try:
                import pygame # self mod (module) (module name) (subsection of module) (name references)
                self.mod_Pygame__ = pygame
                import pygame.locals
                self.mod_Pygame_locals_ = pygame.locals
                from tkinter import messagebox
                self.mod_Tkinter_messagebox_ = messagebox
                import sys
                self.mod_Sys__ = sys

                self.mod_Pygame__.init()
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
                        sys.exit("Thank you for playing")
                    except:
                        quit()

        def GetLoadingCaption(self, num):
            if num == 0:
                self.mod_Pygame__.display.set_caption(f"Pycraft: v{self.version} | Loading (-)")
            elif num == 1:
                self.mod_Pygame__.display.set_caption(f"Pycraft: v{self.version} | Loading (\)")
            elif num == 2:
                self.mod_Pygame__.display.set_caption(f"Pycraft: v{self.version} | Loading (|)")
            elif num == 3:
                self.mod_Pygame__.display.set_caption(f"Pycraft: v{self.version} | Loading (/)")
            else:
                self.mod_Pygame__.display.set_caption(f"Pycraft: v{self.version} | Loading")
            self.mod_Pygame__.display.update()

        def GetNormalCaption(self, location):
            if self.Devmode >= 5 and self.Devmode <= 9:
                self.mod_Pygame__.display.set_caption(f"Pycraft: v{self.version}: {location} | you are: {10-self.Devmode} steps away from being a developer") 
            elif self.Devmode == 10: 
                self.mod_Pygame__.display.set_caption(f"Pycraft: v{self.version}: {location} | Developer Mode | V: 0, 0, 0 | FPS: {self.FPS} eFPS: {int(self.eFPS)} aFPS: {self.aFPS/self.Iteration} | MemUsE: {self.mod_Psutil__.virtual_memory().percent} | CPUUsE: {self.mod_Psutil__.cpu_percent()} | Theme: {self.theme}") 
            else:
                self.mod_Pygame__.display.set_caption(f"Pycraft: v{self.version}: {location}")

else:
    print("You need to run this as part of Pycraft")
    import tkinter as tk
    from tkinter import messagebox
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Startup Fail", "You need to run this as part of Pycraft, please run the 'main.py' file")
    quit()