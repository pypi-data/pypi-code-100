if not __name__ == "__main__":
    print("Started <Pycraft_OGLBenchmark>")
    class LoadOGLBenchmark:
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
                self.mod_Pygame_locals_ = self.mod_Pygame__.locals
                import psutil
                self.mod_Psutil__ = psutil
                from tkinter import messagebox
                self.mod_Tkinter_messagebox_ = messagebox
                import OpenGL.GL
                self.mod_OpenGL_GL_ = OpenGL.GL
                import OpenGL.GLU
                self.mod_OpenGL_GLU_ = OpenGL.GLU
                
                self.mod_Pygame__.init()
                
                base_folder = os.path.dirname(__file__)
            except Exception as error:
                print(error)
                try:
                    import tkinter as tk
                    root = tk.Tk()
                    root.withdraw()
                    self.mod_Tkinter_messagebox_showerror("Startup Fail", "Missing required modules")
                    quit()
                except:
                    try:
                        self.mod_Pygame__.quit()
                        sys.exit("Thank you for playing")
                    except:
                        quit()

        def Cube(self, edges, vertices):
            self.mod_OpenGL_GL_.glBegin(self.mod_OpenGL_GL_.GL_LINES)
            for edge in edges:
                for vertex in edge:
                    self.mod_OpenGL_GL_.glVertex3fv(vertices[vertex])
            self.mod_OpenGL_GL_.glEnd()

        def CreateBenchmark(self):
            self.mod_OpenGL_GLU_.gluPerspective(45, (1280/720), 0.1, 50.0)
            self.mod_OpenGL_GL_.glTranslatef(0.0,0.0, -5)

        def RunBenchmark(self, edges, vertices):
            self.mod_OpenGL_GL_.glRotatef(1, 3, 1, 1)
            self.mod_OpenGL_GL_.glClear(self.mod_OpenGL_GL_.GL_COLOR_BUFFER_BIT|self.mod_OpenGL_GL_.GL_DEPTH_BUFFER_BIT)
            LoadOGLBenchmark.Cube(self, edges, vertices)
else:
    print("You need to run this as part of Pycraft")
    import tkinter as tk
    from tkinter import messagebox
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Startup Fail", "You need to run this as part of Pycraft, please run the 'main.py' file")
    quit()