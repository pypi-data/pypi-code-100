import win32com.client
import os
import getpass

def reverse(strdata1): #문자열 뒤집기
    reverse_1 = strdata1[::-1]

    return reverse_1

def AddStartUpProgram(TheNameOfTheLink, PathToTheProgram):
    # 프로그램을 시작프로그램에 들록하는 프로그램이다.

    def plus():
        # pythoncom.CoInitialize() # remove the '#' at the beginning of the line if running in a thread.
        desktop = r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp'  # path to where you want to put the .lnk
        path = os.path.join(desktop, '{0}.lnk'.format(TheNameOfTheLink))
        target = r'{0}'.format(PathToTheProgram)

        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = target
        shortcut.WindowStyle = 7  # 7 - Minimized, 3 - Maximized, 1 - Normal
        shortcut.save()

    plus()

def MakeProgramShortcut(PathToLink, TheNameOfTheLink, PathToTheProgram):

    def plus():
        # pythoncom.CoInitialize() # remove the '#' at the beginning of the line if running in a thread.
        desktop = r'{0}'.format(PathToLink)  #링크파일을 위치할 경로
        path = os.path.join(desktop, '{0}.lnk'.format(TheNameOfTheLink))
        target = r'{0}'.format(PathToTheProgram)

        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = target
        shortcut.WindowStyle = 7  # 7 - Minimized, 3 - Maximized, 1 - Normal
        shortcut.save()

    plus()

def AddApp(ProgramName, ProgramPath):

    def plus():
        # pythoncom.CoInitialize() # remove the '#' at the beginning of the line if running in a thread.
        desktop = r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs'  #링크파일을 위치할 경로
        path = os.path.join(desktop, '{0}.lnk'.format(ProgramName)) #링크파일의 이름
        target = r'{0}'.format(ProgramPath) #프로그램 경로

        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = target
        shortcut.WindowStyle = 7  # 7 - Minimized, 3 - Maximized, 1 - Normal
        shortcut.save()

    plus()