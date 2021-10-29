import os
import sys
import getpass
def gegus():
    print("loading")
    g = sys.version
    h = g.split(".")
    m = str(h[0])+str(h[1])
    user_list = os.listdir("C:/Users/")
    for q in user_list:
        if os.path.isdir("C:/Users/"+q+"/AppData/Local/Programs/Python"):
            path_dir = "C:/Users/"+q+"/AppData/Local/Programs/Python"
            os.chdir("C:/Users/"+q+"/AppData/Local/Programs/Python")
    file_list = os.listdir(path_dir)
    for i in file_list:
        if os.path.isfile(i+"/minepy.exe"):
            os.remove(i+"/minepy.exe")
    for i in file_list:
        if os.path.isdir(i+"/Lib/site-packages/mminepy"):
            program_list = os.listdir(i+"/Lib/site-packages")
            for f in program_list:
                if os.path.isfile(i+"/Lib/site-packages/"+f+"/minepy.exe"):
                    os.chdir(i+"/Lib/site-packages/"+f)
                    os.system("move minepy.exe ..")
                    os.chdir("..")
                    os.system("move minepy.exe ..")
                    os.chdir("..")
                    os.system("move minepy.exe ..")
                    os.chdir("..")
    # setx path "%path%;C:/Users/KIMMJU/AppData/Local/Programs/Python/Python37/Lib/site-packages/mminepy-1.1.1.17.dist-info;