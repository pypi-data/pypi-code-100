if not __name__ == "__main__":
    print("Started <Pycraft_DisplayUtils>")
    class DisplayUtils:
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
                import pyautogui
                self.mod_Pyautogui__ = pyautogui
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
                
        def UpdateDisplay(self): # Run tests to make sure windows not too small
            try:
                try:
                    FullscreenX, FullscreenY = self.mod_Pyautogui__.size()
                    icon = self.mod_Pygame__.image.load(self.mod_OS__.path.join(self.base_folder, ("Resources\\General_Resources\\Icon.jpg"))).convert()
                    self.mod_Pygame__.display.set_icon(icon)
                    if self.Fullscreen == False:
                        self.mod_Pygame__.display.quit()
                        self.mod_Pygame__.init()
                        self.Fullscreen = True
                        self.Display = self.mod_Pygame__.display.set_mode((self.SavedWidth, self.SavedHeight), self.mod_Pygame__.RESIZABLE)
                    elif self.Fullscreen == True:
                        self.mod_Pygame__.display.quit()
                        self.mod_Pygame__.init()
                        self.Fullscreen = False
                        self.Display = self.mod_Pygame__.display.set_mode((FullscreenX, FullscreenY), self.mod_Pygame__.FULLSCREEN|self.mod_Pygame__.HWSURFACE|self.mod_Pygame__.DOUBLEBUF)
                except Exception as error:
                    self.Fullscreen = True
                    self.SavedWidth = 1280
                    self.SavedHeight = 720
                    self.mod_Pygame__.display.quit()
                    self.mod_Pygame__.init()
                    self.Display = self.mod_Pygame__.display.set_mode((self.SavedWidth, self.SavedHeight))
                icon = self.mod_Pygame__.image.load(self.mod_OS__.path.join(self.base_folder, ("Resources\\General_Resources\\Icon.jpg"))).convert()
                self.mod_Pygame__.display.set_icon(icon)
            except Exception as Message:
                return Message
            else:
                return None

        def SetOPENGLdisplay(self):
            try:
                try:
                    FullscreenX, FullscreenY = self.mod_Pyautogui__.size()
                    icon = self.mod_Pygame__.image.load(self.mod_OS__.path.join(self.base_folder, ("Resources\\General_Resources\\Icon.jpg"))).convert()
                    self.mod_Pygame__.display.set_icon(icon)
                    if self.Fullscreen == True:
                        self.mod_Pygame__.display.quit()
                        self.mod_Pygame__.init()
                        self.Display = self.mod_Pygame__.display.set_mode((self.SavedWidth, self.SavedHeight), self.mod_Pygame__.DOUBLEBUF|self.mod_Pygame__.OPENGL)
                    elif self.Fullscreen == False:
                        self.mod_Pygame__.display.quit()
                        self.mod_Pygame__.init()
                        self.Display = self.mod_Pygame__.display.set_mode((FullscreenX, FullscreenY), self.mod_Pygame__.FULLSCREEN|self.mod_Pygame__.HWSURFACE|self.mod_Pygame__.DOUBLEBUF|self.mod_Pygame__.OPENGL)
                except Exception as error:
                    self.SavedWidth = 1280
                    self.SavedHeight = 720
                    self.mod_Pygame__.display.quit()
                    self.mod_Pygame__.init()
                    self.Display = self.mod_Pygame__.display.set_mode((self.SavedWidth, self.SavedHeight), self.mod_Pygame__.DOUBLEBUF|self.mod_Pygame__.OPENGL)
                icon = self.mod_Pygame__.image.load(self.mod_OS__.path.join(self.base_folder, ("Resources\\General_Resources\\Icon.jpg"))).convert()
                self.mod_Pygame__.display.set_icon(icon)
            except Exception as Message:
                return Message
            else:
                return None
        
        def UpdateOPENGLdisplay(self):
            try:
                try:
                    FullscreenX, FullscreenY = self.mod_Pyautogui__.size()
                    icon = self.mod_Pygame__.image.load(self.mod_OS__.path.join(self.base_folder, ("Resources\\General_Resources\\Icon.jpg"))).convert()
                    self.mod_Pygame__.display.set_icon(icon)
                    if self.Fullscreen == False:
                        self.mod_Pygame__.display.quit()
                        self.mod_Pygame__.init()
                        self.Fullscreen = True
                        self.Display = self.mod_Pygame__.display.set_mode((self.SavedWidth, self.SavedHeight), self.mod_Pygame__.DOUBLEBUF|self.mod_Pygame__.OPENGL)
                    elif self.Fullscreen == True:
                        self.mod_Pygame__.display.quit()
                        self.mod_Pygame__.init()
                        self.Fullscreen = False
                        self.Display = self.mod_Pygame__.display.set_mode((FullscreenX, FullscreenY), self.mod_Pygame__.FULLSCREEN|self.mod_Pygame__.HWSURFACE|self.mod_Pygame__.DOUBLEBUF|self.mod_Pygame__.OPENGL)
                except Exception as error:
                    self.SavedWidth = 1280
                    self.SavedHeight = 720
                    self.mod_Pygame__.display.quit()
                    self.mod_Pygame__.init()
                    self.Fullscreen = False
                    self.Display = self.mod_Pygame__.display.set_mode((self.SavedWidth, self.SavedHeight), self.mod_Pygame__.DOUBLEBUF|self.mod_Pygame__.OPENGL)
                icon = self.mod_Pygame__.image.load(self.mod_OS__.path.join(self.base_folder, ("Resources\\General_Resources\\Icon.jpg"))).convert()
                self.mod_Pygame__.display.set_icon(icon)
            except Exception as Message:
                return Message
            else:
                return None

        def SetDisplay(self):
            try:
                try:
                    FullscreenX, FullscreenY = self.mod_Pyautogui__.size()
                    if self.Fullscreen == True:
                        self.mod_Pygame__.display.quit()
                        self.mod_Pygame__.init()
                        self.Display = self.mod_Pygame__.display.set_mode((self.SavedWidth, self.SavedHeight), self.mod_Pygame__.RESIZABLE)
                    elif self.Fullscreen == False:
                        self.mod_Pygame__.display.quit()
                        self.mod_Pygame__.init()
                        self.Display = self.mod_Pygame__.display.set_mode((FullscreenX, FullscreenY), self.mod_Pygame__.FULLSCREEN|self.mod_Pygame__.HWSURFACE|self.mod_Pygame__.DOUBLEBUF)
                except Exception as error:
                    self.SavedWidth = 1280
                    self.SavedHeight = 720
                    self.mod_Pygame__.display.quit()
                    self.mod_Pygame__.init()
                    self.Display = self.mod_Pygame__.display.set_mode((self.SavedWidth, self.SavedHeight))
                icon = self.mod_Pygame__.image.load(self.mod_OS__.path.join(self.base_folder, ("Resources\\General_Resources\\Icon.jpg"))).convert()
                self.mod_Pygame__.display.set_icon(icon)
            except Exception as Message:
                return Message
            else:
                return None

        def GenerateMinDisplay(self, width, height):
            try:
                self.Display = self.mod_Pygame__.display.set_mode((width, height), self.mod_Pygame__.RESIZABLE)
                icon = self.mod_Pygame__.image.load(self.mod_OS__.path.join(self.base_folder, ("Resources\\General_Resources\\Icon.jpg"))).convert()
                self.mod_Pygame__.display.set_icon(icon)
            except Exception as Message:
                return Message
            else:
                return None

        def GetDisplayLocation(self):
            hwnd = self.mod_Pygame__.display.get_wm_info()["window"]

            prototype = self.mod_Ctypes__.WINFUNCTYPE(self.mod_Ctypes__.wintypes.BOOL, self.mod_Ctypes__.wintypes.HWND, self.mod_Ctypes__.POINTER(self.mod_Ctypes__.wintypes.RECT))
            paramflags = (1, "hwnd"), (2, "lprect")

            GetWindowRect = prototype(("GetWindowRect", self.mod_Ctypes__.windll.user32), paramflags)

            rect = GetWindowRect(hwnd)

            return rect.left+8, rect.top+31

        def GetPlayStatus(self):
            if self.mod_Pygame__.display.get_active() == True:
                tempFPS = self.FPS
                self.mod_Pygame__.mixer.Channel(2).unpause()
                if self.mod_Pygame__.mixer.Channel(2).get_busy() == 0 and self.LoadMusic == True:
                    if self.music == True or self.CurrentlyPlaying == None:
                        self.CurrentlyPlaying = "InvSound"
                        self.LoadMusic = False
                        MusicThread = self.mod_Threading__.Thread(target=self.mod_SoundUtils__.PlaySound.PlayInvSound, args=(self,))
                        MusicThread.start()
            else:
                self.LoadMusic = True
                tempFPS = 15
                self.mod_Pygame__.mixer.Channel(2).pause()
            return tempFPS

        def GenerateLoadDisplay(self, LoadingFont, text, MessageText, LoadingPercent, eventHandle, MainTitleFont, SecondaryFont, LoadingTextFont, line):
            self.Display.fill(self.BackgroundCol)

            realWidth, realHeight = self.mod_Pygame__.display.get_window_size()
            yScaleFact = realHeight/720
            xScaleFact = realWidth/1280

            PycraftTitle = MainTitleFont.render("Pycraft", self.aa, self.FontCol)
            TitleWidth = PycraftTitle.get_width()
            self.Display.blit(PycraftTitle, ((realWidth-TitleWidth)/2, 0))

            LoadingTitle = SecondaryFont.render("Loading", self.aa, self.FontCol)
            self.Display.blit(LoadingTitle, (((realWidth-TitleWidth)/2)+55, 50))

            line.append((LoadingPercent, realHeight-100))
            self.mod_Pygame__.draw.lines(self.Display, (self.ShapeCol), self.aa, [(100, realHeight-100), (realWidth-100, realHeight-100)], 3)
            self.mod_Pygame__.draw.lines(self.Display, (self.AccentCol), self.aa, line)

            DisplayMessage = LoadingFont.render(MessageText, self.aa, self.FontCol)
            DisplayMessageWidth = DisplayMessage.get_width()
            self.Display.blit(DisplayMessage, ((realWidth-DisplayMessageWidth)/2, realHeight-120))

            TextFontRendered = LoadingTextFont.render(f"{text}", self.aa, self.FontCol)
            TextFontRenderedWidth = TextFontRendered.get_width()
            self.Display.blit(TextFontRendered, ((realWidth-TextFontRenderedWidth)/2, realHeight-100))

            self.mod_Pygame__.display.flip()

            if eventHandle == True:
                self.mod_Pygame__.event.get()
else:
    print("You need to run this as part of Pycraft")
    import tkinter as tk
    from tkinter import messagebox
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Startup Fail", "You need to run this as part of Pycraft, please run the 'main.py' file")
    quit()