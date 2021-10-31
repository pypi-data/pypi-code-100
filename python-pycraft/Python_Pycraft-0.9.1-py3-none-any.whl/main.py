print("Started <Pycraft_main>")
class Startup:
    def __init__(Class_Startup_variables):
        try:
            import tkinter as tk
            Class_Startup_variables.mod_Tkinter__tk = tk # [Class_Startup_variables] mod (module) (module name) (subsection of module) (name references)
            import tkinter.ttk # Class _ <class_name> _ variables
            Class_Startup_variables.mod_Tkinter_ttk_ = tkinter.ttk
            from tkinter import messagebox
            Class_Startup_variables.mod_Tkinter_messagebox_ = messagebox
            from PIL import Image, ImageTk, ImageGrab
            Class_Startup_variables.mod_PIL_Image_ = Image
            Class_Startup_variables.mod_PIL_ImageTk_ = ImageTk
            Class_Startup_variables.mod_PIL_ImageGrab_ = ImageGrab
            import pygame
            Class_Startup_variables.mod_Pygame__ = pygame
            import numpy
            Class_Startup_variables.mod_Numpy__ = numpy
            import os
            Class_Startup_variables.mod_OS__ = os
            import sys
            Class_Startup_variables.mod_Sys__ = sys
            import random
            Class_Startup_variables.mod_Random__ = random
            import time
            Class_Startup_variables.mod_Time__ = time
            import pygame.locals
            Class_Startup_variables.mod_Pygame_locals_ = pygame.locals
            import OpenGL.GL
            Class_Startup_variables.mod_OpenGL_GL_ = OpenGL.GL
            import OpenGL.GLU
            Class_Startup_variables.mod_OpenGL_GLU_ = OpenGL.GLU
            import OpenGL.GLUT
            Class_Startup_variables.mod_OpenGL_GLUT_ = OpenGL.GLUT
            import pyautogui
            Class_Startup_variables.mod_Pyautogui__ = pyautogui
            import psutil
            Class_Startup_variables.mod_Psutil__ = psutil
            import pywavefront
            Class_Startup_variables.mod_Pywavefront__ = pywavefront
            import timeit
            Class_Startup_variables.mod_Timeit__ = timeit
            import subprocess
            Class_Startup_variables.mod_Subprocess__ = subprocess
            import traceback
            Class_Startup_variables.mod_Traceback__ = traceback
            import datetime
            Class_Startup_variables.mod_Datetime__ = datetime
            import ctypes
            Class_Startup_variables.mod_Ctypes__ = ctypes
            import json
            Class_Startup_variables.mod_JSON__ = json
            import threading
            Class_Startup_variables.mod_Threading__ = threading
            import cpuinfo
            Class_Startup_variables.mod_CPUinfo__ = cpuinfo
            import array
            Class_Startup_variables.mod_Array__ = array

            Class_Startup_variables.mod_Pygame__.init()
            
            import Pycraft.PycraftStartupTest
            Class_Startup_variables.mod_PycraftStartupTest__ = Pycraft.PycraftStartupTest
            import Pycraft.StartupAnimation
            Class_Startup_variables.mod_StartupAnimation__ = Pycraft.StartupAnimation
            import Pycraft.DisplayUtils
            Class_Startup_variables.mod_DisplayUtils__ = Pycraft.DisplayUtils
            import Pycraft.GetSavedData
            Class_Startup_variables.mod_GetSavedData__ = Pycraft.GetSavedData
            import Pycraft.ThemeUtils
            Class_Startup_variables.mod_ThemeUtils__ = Pycraft.ThemeUtils
            import Pycraft.HomeScreen
            Class_Startup_variables.mod_HomeScreen__ = Pycraft.HomeScreen
            import Pycraft.SoundUtils
            Class_Startup_variables.mod_SoundUtils__ = Pycraft.SoundUtils
            import Pycraft.DrawingUtils
            Class_Startup_variables.mod_DrawingUtils__ = Pycraft.DrawingUtils
            import Pycraft.CaptionUtils
            Class_Startup_variables.mod_CaptionUtils__ = Pycraft.CaptionUtils
            import Pycraft.Credits
            Class_Startup_variables.mod_Credits__ = Pycraft.Credits
            import Pycraft.TkinterUtils
            Class_Startup_variables.mod_TkinterUtils__ = Pycraft.TkinterUtils
            import Pycraft.Achievements
            Class_Startup_variables.mod_Achievements__ = Pycraft.Achievements
            import Pycraft.CharacterDesigner
            Class_Startup_variables.mod_CharacterDesigner__ = Pycraft.CharacterDesigner
            import Pycraft.Settings
            Class_Startup_variables.mod_Settings__ = Pycraft.Settings
            import Pycraft.Benchmark
            Class_Startup_variables.mod_Benchmark__ = Pycraft.Benchmark
            import Pycraft.ExBenchmark
            Class_Startup_variables.mod_ExBenchmark__ = Pycraft.ExBenchmark
            import Pycraft.OGLbenchmark
            Class_Startup_variables.mod_OGLbenchmark__ = Pycraft.OGLbenchmark
            import Pycraft.MainGameEngine
            Class_Startup_variables.mod_MainGameEngine__ = Pycraft.MainGameEngine
            import Pycraft.TextUtils
            Class_Startup_variables.mod_TextUtils__ = Pycraft.TextUtils
            import Pycraft.ModelMathsUtil
            Class_Startup_variables.mod_ModelMathsUtil__ = Pycraft.ModelMathsUtil
            import Pycraft.SkyBoxUtil
            Class_Startup_variables.mod_SkyBoxUtil__ = Pycraft.SkyBoxUtil
            import Pycraft.MapTextureUtil
            Class_Startup_variables.mod_MapTextureUtil__ = Pycraft.MapTextureUtil
            import Pycraft.GetWorldCollisions
            Class_Startup_variables.mod_GetWorldCollisions__ = Pycraft.GetWorldCollisions
            import Pycraft.GetWorldVertex
            Class_Startup_variables.mod_GetWorldVertex__ = Pycraft.GetWorldVertex
            import Pycraft.Inventory
            Class_Startup_variables.mod_Inventory__ = Pycraft.Inventory
            import Pycraft.ImageUtils
            Class_Startup_variables.mod_ImageUtils__ = Pycraft.ImageUtils
            import Pycraft.MapGUI
            Class_Startup_variables.mod_MapGUI__ = Pycraft.MapGUI

            import Pycraft.SetCollisionData
            Class_Startup_variables.mod_SetCollisionData__ = Pycraft.SetCollisionData
            Class_Startup_variables.Map_collisions = Class_Startup_variables.mod_SetCollisionData__.SetMapCollisions.__init__()

            import Pycraft.SetVertexData
            Class_Startup_variables.mod_SetVertexData__ = Pycraft.SetVertexData
            Class_Startup_variables.Map_IterableVertices = Class_Startup_variables.mod_SetVertexData__.SetMapVertices.__init__()

            Class_Startup_variables.aa = True
            Class_Startup_variables.AccentCol = (237, 125, 49)
            Class_Startup_variables.aFPS = 0
            Class_Startup_variables.BackgroundCol = [30, 30, 30]
            Class_Startup_variables.base_folder = os.path.dirname(__file__)
            Class_Startup_variables.cameraANGspeed = 3.5
            Class_Startup_variables.clock = pygame.time.Clock()
            Class_Startup_variables.crash = False
            Class_Startup_variables.CurrentlyPlaying = None
            Class_Startup_variables.Devmode = 0
            Class_Startup_variables.Display = 0
            Class_Startup_variables.eFPS = 60
            Class_Startup_variables.FanSky = True
            Class_Startup_variables.FanPart = True
            Class_Startup_variables.FontCol = (255, 255, 255)
            Class_Startup_variables.FOV = 70
            Class_Startup_variables.Fullscreen = False
            Class_Startup_variables.FPS = 60
            Class_Startup_variables.FullscreenX, Class_Startup_variables.FullscreenY = pyautogui.size()
            Class_Startup_variables.G3Dscale = 600000
            Class_Startup_variables.Iteration = 0
            Class_Startup_variables.lastRun = "29/09/2021"
            Class_Startup_variables.Load3D = True
            Class_Startup_variables.LoadMusic = True
            Class_Startup_variables.Map = 0
            Class_Startup_variables.Map_box = 0
            Class_Startup_variables.Map_scale = 0
            Class_Startup_variables.Map_size = 0
            Class_Startup_variables.Map_trans = 0
            Class_Startup_variables.MapVerts = 0
            Class_Startup_variables.max_Map_size = 0
            Class_Startup_variables.max_v = 0
            Class_Startup_variables.min_v = 0
            Class_Startup_variables.music = True
            Class_Startup_variables.musicVOL = 5
            Class_Startup_variables.RenderFOG = True
            Class_Startup_variables.RunFullStartup = False
            Class_Startup_variables.SavedWidth = 1280
            Class_Startup_variables.SavedHeight = 720
            Class_Startup_variables.ShapeCol = (80, 80, 80)
            Class_Startup_variables.sound = True
            Class_Startup_variables.soundVOL = 75
            Class_Startup_variables.theme = False
            Class_Startup_variables.version = "0.9.1"
            Class_Startup_variables.X = 0
            Class_Startup_variables.Y = 0
            Class_Startup_variables.Z = 0
        except Exception as error:
            print(error)
            try:
                import tkinter as tk
                root = tk.Tk()
                root.withdraw()
                Class_Startup_variables.mod_Tkinter_messagebox_.showerror("Startup Fail", "Missing required modules")
                quit()
            except:
                try:
                    Class_Startup_variables.mod_Pygame__.quit()
                    sys.exit("0.0 -Thank you for playing")
                except:
                    quit()
                    
    def crash(ErrorREPORT):
        if not ErrorREPORT == None:
            Class_Startup_variables.mod_Pygame__.init()
            Class_Startup_variables.mod_Pygame__.mixer.stop()
            try:
                Message = Class_Startup_variables.mod_GetSavedData__.LoadSaveFiles.SaveTOconfigFILE(Class_Startup_variables)
                Class_Startup_variables.mod_Pygame__.display.quit()
                Class_Startup_variables.mod_Pygame__.init()
                Display = Class_Startup_variables.mod_Pygame__.display.set_mode((1280, 720))
                icon = Class_Startup_variables.mod_Pygame__.image.load(Class_Startup_variables.mod_OS__.path.join(Class_Startup_variables.base_folder, ("Resources\\General_Resources\\Icon.jpg"))).convert()
                Class_Startup_variables.mod_Pygame__.display.set_icon(icon)
                Class_Startup_variables.mod_Pygame__.display.set_caption(f"Pycraft: An Error Occurred")

                MessageFont = Class_Startup_variables.mod_Pygame__.font.Font(Class_Startup_variables.mod_OS__.path.join(Class_Startup_variables.base_folder,("Fonts\\Book Antiqua.ttf")), 15)

                ErrorMessageText = MessageFont.render(str(ErrorREPORT), True, (255,0,0))
                ErrorMessageTextWidth = ErrorMessageText.get_width()
                ErrorMessageTextHeight = ErrorMessageText.get_height()
                Display = Class_Startup_variables.mod_Pygame__.display.set_mode((1280,720))

                IconImage = Class_Startup_variables.mod_Pygame__.image.load(Class_Startup_variables.mod_OS__.path.join(Class_Startup_variables.base_folder,("Resources\\Error_Resources\\Icon.jpg")))
                Class_Startup_variables.mod_Pygame__.display.set_icon(IconImage)
                image = Class_Startup_variables.mod_Pygame__.image.load(Class_Startup_variables.mod_OS__.path.join(Class_Startup_variables.base_folder,("Resources\\Error_Resources\\Error_Message.png")))
                Clock = Class_Startup_variables.mod_Pygame__.time.Clock()
                while True:
                    Display.fill((20,20,20))
                    Display.blit(image, (0,0))

                    Display.blit(ErrorMessageText, ((((1280/2)-ErrorMessageTextWidth)/2), (720-ErrorMessageTextHeight)/2))

                    for event in Class_Startup_variables.mod_Pygame__.event.get():
                        if event.type == Class_Startup_variables.mod_Pygame__.QUIT:
                            Class_Startup_variables.mod_Pygame__.quit()
                            Class_Startup_variables.mod_Sys__.exit(f"0.1- Thank you for playing")
                    Class_Startup_variables.mod_Pygame__.display.flip()
                    Clock.tick(30)
            except Exception as error:
                Class_Startup_variables.mod_Sys__.exit(f"0.2- {error} Thank you for playing")
        else:
            try:
                Class_Startup_variables.mod_Pygame__.quit()
            except Exception as error:
                Class_Startup_variables.mod_Sys__.exit(f"0.3- {error} Thank you for playing")
                quit()
            else:
                Class_Startup_variables.mod_Sys__.exit("0.4- Thank you for playing")
                quit()

Class_Startup_variables = Startup()
try:
    Class_Startup_variables.mod_GetSavedData__.LoadSaveFiles.ReadMainSave(Class_Startup_variables)
except Exception as FileError:
    try:
        if str(FileError) == "Expecting value: line 1 column 1 (char 0)":
            Report = Class_Startup_variables.mod_GetSavedData__.LoadSaveFiles.RepairLostSave(Class_Startup_variables)
            ErrorString = "Unable to access vital Saved Data, have attempted a fix successfully", FileError
            Message = "0.0- " + str(ErrorString)
            Startup.crash(Message)
    except Exception as Error:
        Message = "0.1- " + str(Error)
        Startup.crash(Message)

    Message = "0.2- " + str(FileError)
    Startup.crash(Message)

Message = Class_Startup_variables.mod_PycraftStartupTest__.StartupTest.PycraftSelfTest(Class_Startup_variables)
if not Message == None:
    Message = "0.4- " + str(Message)
    Startup.crash(Message)

if Class_Startup_variables.theme == False:
    Message = Class_Startup_variables.mod_ThemeUtils__.DetermineThemeColours.GetThemeGUI(Class_Startup_variables)
    if not Message == None:
        Message = "0.4- " + str(Message)
        Startup.crash(Message)

Message = Class_Startup_variables.mod_ThemeUtils__.DetermineThemeColours.GetColours(Class_Startup_variables)

if not Message == None:
    Message = "0.5- " + str(Message)
    Startup.crash(Message)
    
Message = Class_Startup_variables.mod_StartupAnimation__.GenerateStartupScreen.Start(Class_Startup_variables)
if not Message == None:
    Message = "0.6- " + str(Message)
    Startup.crash(Message)

Command = "Undefined"
while True:
    if Command == "saveANDexit":
        Message = Class_Startup_variables.mod_GetSavedData__.LoadSaveFiles.SaveTOconfigFILE(Class_Startup_variables)
        if not Message == None:
            Message = "0.8- " + str(Message)
            Startup.crash(Message)
        else:
            Class_Startup_variables.mod_Pygame__.quit()
            Class_Startup_variables.mod_Sys__.exit("0.5- Thank you for playing") # 0 = Order of running, 5 = 5th occurrence down page
    elif Command == "Credits":
        Message = Class_Startup_variables.mod_Credits__.GenerateCredits.Credits(Class_Startup_variables)
        if not Message == None:
            Message = "0.9- " + str(Message)
            Startup.crash(Message)
        Command = "Undefined"
    elif Command == "Achievements":
        Message = Class_Startup_variables.mod_Achievements__.GenerateAchievements.Achievements(Class_Startup_variables)
        if not Message == None:
            Message = "0.10- " + str(Message)
            Startup.crash(Message)
        Command = "Undefined"
    elif Command == "CharacterDesigner":
        Message = Class_Startup_variables.mod_CharacterDesigner__.GenerateCharacterDesigner.CharacterDesigner(Class_Startup_variables)
        if not Message == None:
            Message = "0.11- " + str(Message)
            Startup.crash(Message)
        Command = "Undefined"
    elif Command == "Settings":
        Message = Class_Startup_variables.mod_Settings__.GenerateSettings.settings(Class_Startup_variables)
        if not Message == None:
            Message = "0.12- " + str(Message)
            Startup.crash(Message)
        Command = "Undefined"
    elif Command == "Benchmark":
        Message = Class_Startup_variables.mod_Benchmark__.GenerateBenchmarkMenu.Benchmark(Class_Startup_variables)
        if not Message == None:
            Message = "0.13- " + str(Message)
            Startup.crash(Message)
        Command = "Undefined"
    elif Command == "Play":
        Message, Command = Class_Startup_variables.mod_MainGameEngine__.CreateEngine.Play(Class_Startup_variables)
        if not Message == None:
            Message = "0.14- " + str(Message)
            Startup.crash(Message)
        Message = Class_Startup_variables.mod_DisplayUtils__.DisplayUtils.SetDisplay(Class_Startup_variables)
        if not Message == None:
            Message = "0.15- " + str(Message)
            Startup.crash(Message)
    elif Command == "Inventory":
        Message = Class_Startup_variables.mod_Inventory__.GenerateInventory.Inventory(Class_Startup_variables)
        if not Message == None:
            Message = "0.16- " + str(Message)
            Startup.crash(Message)
        Command = "Play"
    elif Command == "MapGUI":
        Message = Class_Startup_variables.mod_MapGUI__.GenerateMapGUI.MapGUI(Class_Startup_variables)
        if not Message == None:
            Message = "0.17- " + str(Message)
            Startup.crash(Message)
        Command = "Play"
    else:
        Message, Command = Class_Startup_variables.mod_HomeScreen__.GenerateHomeScreen.Home_Screen(Class_Startup_variables)
        if not Message == None:
            Message = "0.7- " + str(Message)
            Startup.crash(Message)
