if not __name__ == "__main__":
    print("Started <Pycraft_CharacterDesigner>")
    class GenerateCharacterDesigner:
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
                import psutil
                self.mod_Psutil__ = psutil
                from tkinter import messagebox
                self.mod_Tkinter_messagebox_ = messagebox
                
                self.mod_Pygame__.init()
                
                self.base_folder = os.path.dirname(__file__)
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

        def CharacterDesigner(self):
            try:
                self.Display.fill(self.BackgroundCol) 
                self.mod_Pygame__.display.flip()
                self.mod_CaptionUtils__.GenerateCaptions.GetNormalCaption(self, "Character Designer")
                MainTitleFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts\\Book Antiqua.ttf")), 60) 
                InfoTitleFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts\\Book Antiqua.ttf")), 35)
                DataFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts\\Book Antiqua.ttf")), 15)
                data1 = []
                data2 = []
                data3 = []
                data4 = []

                run = 0
                rerun = 0
                TitleFont = MainTitleFont.render("Pycraft", self.aa, self.FontCol)
                TitleWidth = TitleFont.get_width()

                AchievementsFont = InfoTitleFont.render("Character Designer", self.aa, self.FontCol)
                tempFPS = self.FPS

                while True:
                    realWidth, realHeight = self.mod_Pygame__.display.get_window_size()

                    if realWidth < 1280:
                        self.mod_DisplayUtils__.DisplayUtils.GenerateMinDisplay(self, 1280, self.SavedHeight)
                    if realHeight < 720:
                        self.mod_DisplayUtils__.DisplayUtils.GenerateMinDisplay(self, self.SavedWidth, 720)

                    self.eFPS = self.clock.get_fps()
                    self.aFPS += self.eFPS 
                    run += 1
                    self.Iteration += 1
                    
                    tempFPS = self.mod_DisplayUtils__.DisplayUtils.GetPlayStatus(self)

                    for event in self.mod_Pygame__.event.get(): 
                        if event.type == self.mod_Pygame__.QUIT or (event.type == self.mod_Pygame__.KEYDOWN and event.key == self.mod_Pygame__.K_ESCAPE): 
                            if self.sound == True:
                                self.mod_SoundUtils__.PlaySound.PlayClickSound(self)
                            return None
                        elif event.type == self.mod_Pygame__.KEYDOWN: 
                            if event.key == self.mod_Pygame__.K_SPACE and self.Devmode < 10: 
                                self.Devmode += 1 
                            if event.key == self.mod_Pygame__.K_q:
                                self.mod_TkinterUtils__.TkinterInfo.CreateTkinterWindow(self)
                            if event.key == self.mod_Pygame__.K_F11:
                                self.mod_DisplayUtils__.DisplayUtils.UpdateDisplay(self)
                            if event.key == self.mod_Pygame__.K_x: 
                                self.Devmode = 1 

                    self.mod_CaptionUtils__.GenerateCaptions.GetNormalCaption(self, "Character Designer")
                            
                    self.Display.fill(self.BackgroundCol)

                    cover_Rect = self.mod_Pygame__.Rect(0, 0, 1280, 90)
                    self.mod_Pygame__.draw.rect(self.Display, (self.BackgroundCol), cover_Rect)
                    self.Display.blit(TitleFont, ((realWidth-TitleWidth)/2, 0))
                    self.Display.blit(AchievementsFont, (((realWidth-TitleWidth)/2)+55, 50))
                    if run >= 1000:
                        run = 0
                        rerun += 1
                    Message = self.mod_DrawingUtils__.GenerateGraph.CreateDevmodeGraph(self, run, rerun, data1, data2, data3, data4, DataFont)
                    if not Message == None:
                        return Message
                    self.mod_Pygame__.display.flip() 
                    self.clock.tick(tempFPS)
            except Exception as Message:
                return Message
else:
    print("You need to run this as part of Pycraft")
    import tkinter as tk
    from tkinter import messagebox
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Startup Fail", "You need to run this as part of Pycraft, please run the 'main.py' file")
    quit()