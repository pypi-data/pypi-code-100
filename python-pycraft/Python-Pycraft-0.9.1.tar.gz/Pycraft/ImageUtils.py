if not __name__ == "__main__":
    print("Started <Pycraft_ImageUtils>")
    class ConvertImage:
        def __init__(self):
            try:
                import pygame # self mod (module) (module name) (subsection of module) (name references)
                self.mod_Pygame__ = pygame
                import pygame.locals
                self.mod_Pygame_locals_ = self.mod_Pygame__.locals
                from tkinter import messagebox
                self.mod_Tkinter_messagebox_ = messagebox
                from PIL import Image, ImageTk, ImageGrab
                self.mod_PIL_Image_ = Image
                self.mod_PIL_ImageTk_ = ImageTk
                self.mod_PIL_ImageGrab_ = ImageGrab
                import sys
                self.mod_Sys__ = sys
                
                self.mod_Pygame__.init()
                
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

        def pilImageToSurface(self, pilImage):
            return self.mod_Pygame__.image.fromstring(pilImage.tobytes(), pilImage.size, pilImage.mode).convert()
else:
    print("You need to run this as part of Pycraft")
    import tkinter as tk
    from tkinter import messagebox
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Startup Fail", "You need to run this as part of Pycraft, please run the 'main.py' file")
    quit()