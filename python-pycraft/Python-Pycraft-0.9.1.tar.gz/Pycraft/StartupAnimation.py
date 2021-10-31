if not __name__ == "__main__":
    print("Started <Pycraft_StartupAnimation>")
    class GenerateStartupScreen:
        def __init__(self):
            try:
                import pygame # self mod (module) (module name) (subsection of module) (name references)
                self.mod_Pygame__ = pygame
                import os
                self.mod_OS__ = os
                import sys
                self.mod_Sys__ = sys
                import random
                self.mod_Random__ = random
                import time
                self.mod_Time__ = time
                import pygame.locals
                self.mod_Pygame_locals_ = pygame.locals
                from tkinter import messagebox
                self.mod_Tkinter_messagebox_ = messagebox
                
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
                        
        def Start(self):
            try:
                self.Display.fill(self.BackgroundCol)
                self.mod_Pygame__.display.flip()
                self.mod_Pygame__.display.set_caption(f"Pycraft: v{self.version} | Welcome")
                PresentsFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts\\Book Antiqua.ttf")), 35)
                PycraftFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts\\Book Antiqua.ttf")), 60)
                NameFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts\\Book Antiqua.ttf")), 45)

                NameText = NameFont.render("Tom Jebbo", True, self.FontCol)
                NameTextWidth = NameText.get_width()
                NameTextHeight = NameText.get_height()

                PresentsText = PresentsFont.render("presents", True, self.FontCol)
                PresentsTextWidth = PresentsText.get_width()

                PycraftText = PycraftFont.render("Pycraft", True, self.FontCol)
                PycraftTextWidth = PycraftText.get_width()
                PycraftTextHeight = PycraftText.get_height()

                iteration = 0
                clock = self.mod_Pygame__.time.Clock()
                if self.RunFullStartup == True:
                    while iteration <= (60*3):
                        realWidth, realHeight = self.mod_Pygame__.display.get_window_size()
                        self.Display.fill(self.BackgroundCol)
                        self.Display.blit(NameText, ((realWidth-NameTextWidth)/2, (realHeight-NameTextHeight)/2))
                        iteration += 1
                        self.mod_Pygame__.display.flip()
                        clock.tick(60)
                        for event in self.mod_Pygame__.event.get():
                            if event.type == self.mod_Pygame__.QUIT:
                                self.mod_Pygame__.quit()
                                self.mod_Sys__.exit("Thanks for playing")
                                quit()
                    iteration = 0

                    while iteration <= (60*2):
                        realWidth, realHeight = self.mod_Pygame__.display.get_window_size()
                        self.Display.fill(self.BackgroundCol)
                        self.Display.blit(NameText, ((realWidth-NameTextWidth)/2, (realHeight-NameTextHeight)/2))
                        self.Display.blit(PresentsText, ((((realWidth-NameTextWidth)/2)+120), ((realHeight-NameTextHeight)/2)+30))
                        iteration += 1
                        self.mod_Pygame__.display.flip()
                        clock.tick(60)
                        for event in self.mod_Pygame__.event.get():
                            if event.type == self.mod_Pygame__.QUIT:
                                self.mod_Pygame__.quit()
                                self.mod_Sys__.exit("Thanks for playing")
                                quit()

                    iteration = 0

                while iteration <= (60*3):
                    realWidth, realHeight = self.mod_Pygame__.display.get_window_size()
                    self.Display.fill(self.BackgroundCol)
                    self.Display.blit(PycraftText, ((realWidth-PycraftTextWidth)/2, (realHeight-PycraftTextHeight)/2))
                    iteration += 1
                    self.mod_Pygame__.display.flip()
                    clock.tick(60)
                    for event in self.mod_Pygame__.event.get():
                        if event.type == self.mod_Pygame__.QUIT:
                            self.mod_Pygame__.quit()
                            self.mod_Sys__.exit("Thanks for playing")
                            quit()

                y = 0
                while True:
                    realWidth, realHeight = self.mod_Pygame__.display.get_window_size()
                    self.Display.fill(self.BackgroundCol)
                    self.Display.blit(PycraftText, ((realWidth-PycraftTextWidth)/2, ((realHeight-PycraftTextHeight)/2)-y))
                    y += 2
                    self.mod_Pygame__.display.flip()
                    clock.tick(60)
                    for event in self.mod_Pygame__.event.get():
                        if event.type == self.mod_Pygame__.QUIT:
                            self.mod_Pygame__.quit()
                            self.mod_Sys__.exit("Thanks for playing")
                            quit()
                    if ((realHeight-PycraftTextHeight)/2)-y <= 0:
                        self.RunFullStartup = False
                        return None
                else:
                    self.RunFullStartup = False
                    return None
            except Exception as Message:
                self.RunFullStartup = False
                return Message
else:
    print("You need to run this as part of Pycraft")
    import tkinter as tk
    from tkinter import messagebox
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Startup Fail", "You need to run this as part of Pycraft, please run the 'main.py' file")
    quit()