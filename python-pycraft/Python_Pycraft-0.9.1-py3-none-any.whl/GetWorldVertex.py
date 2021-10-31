if not __name__ == "__main__":
    print("Started <Pycraft_GetWorldVertex>")
    class GetMapVertices:
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
                import OpenGL.GL
                self.mod_OpenGL_GL_ = OpenGL.GL
                import OpenGL.GLU
                self.mod_OpenGL_GLU_ = OpenGL.GLU
                import OpenGL.GLUT
                self.mod_OpenGL_GLUT_ = OpenGL.GLUT
                
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


        def MapModel(self):
            self.mod_OpenGL_GL_.glPushMatrix() 
            self.mod_OpenGL_GL_.glScalef(*self.Map_scale) 
            self.mod_OpenGL_GL_.glTranslatef(*self.Map_trans)
            for mesh in self.Map.mesh_list: 
                self.mod_OpenGL_GL_.glBegin(self.mod_OpenGL_GL_.GL_TRIANGLES)
                for i in range(0, len(self.Map_IterableVertices)):
                    self.mod_OpenGL_GL_.glVertex3f(*self.Map_IterableVertices[i], sep = ',')
                self.mod_OpenGL_GL_.glEnd()
            self.mod_OpenGL_GL_.glPopMatrix()
else:
    print("You need to run this as part of Pycraft")
    import tkinter as tk
    from tkinter import messagebox
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Startup Fail", "You need to run this as part of Pycraft, please run the 'main.py' file")
    quit()