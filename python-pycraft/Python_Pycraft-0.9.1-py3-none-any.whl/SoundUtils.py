if not __name__ == "__main__":
    print("Started <Pycraft_SoundUtils>")
    class PlaySound:
        def __init__(self):
            try:
                import pygame # self mod (module) (module name) (subsection of module) (name references)
                self.mod_Pygame__ = pygame
                import os
                self.mod_OS__ = os
                import random
                self.mod_Random__ = random
                import pygame.locals
                self.mod_Pygame_locals_ = pygame.locals
                from tkinter import messagebox
                self.mod_Tkinter_messagebox_ = messagebox
                import sys
                self.mod_Sys__ = sys
                
                self.mod_Pygame__.init()
                
                self.self.base_folder = os.path.dirname(__file__)
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

        def PlayClickSound(self):
            channel1 = self.mod_Pygame__.mixer.Channel(0)
            clickMUSIC = self.mod_Pygame__.mixer.Sound(self.mod_OS__.path.join(self.base_folder, ("Resources\\General_Resources\\Click.ogg")))
            channel1.set_volume(self.soundVOL/100)
            channel1.play(clickMUSIC)
            self.mod_Pygame__.time.wait(40)

        def PlayFootstepsSound(self):
            channel2 = self.mod_Pygame__.mixer.Channel(1)
            Footsteps = self.mod_Pygame__.mixer.Sound(self.mod_OS__.path.join(self.base_folder, (f"Resources\\G3_Resources\\GameSounds\\footsteps{self.mod_Random__.randint(0, 5)}.ogg")))
            channel2.set_volume(self.soundVOL/100)
            channel2.play(Footsteps)


        def PlayInvSound(self):
            channel3 = self.mod_Pygame__.mixer.Channel(2)
            InvGen = self.mod_Pygame__.mixer.Sound(self.mod_OS__.path.join(self.base_folder, ("Resources\\General_Resources\\InventoryGeneral.ogg")))
            channel3.set_volume(self.musicVOL/100)
            channel3.play(InvGen)


        def PlayAmbientSound(self):
            channel4 = self.mod_Pygame__.mixer.Channel(3)
            LoadAmb = self.mod_Pygame__.mixer.Sound(self.mod_OS__.path.join(self.base_folder, ("Resources\\G3_Resources\\GameSounds\\FieldAmb.ogg")))
            channel4.set_volume(self.soundVOL/100)
            channel4.play(LoadAmb)
else:
    print("You need to run this as part of Pycraft")
    import tkinter as tk
    from tkinter import messagebox
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Startup Fail", "You need to run this as part of Pycraft, please run the 'main.py' file")
    quit()