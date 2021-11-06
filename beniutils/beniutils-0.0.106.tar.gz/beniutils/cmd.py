import os
import sys

from . import (copy, getPath, makeFolder, makeTempWorkspace, readFile,
               remove, writeFile)
from .byte import decode
from .zip import zipFileExtract
from .execute import execute


def main():
    parList = sys.argv[1:]
    if parList:
        funcName = parList.pop(0)
        if funcName not in funcNameList:
            exit(f"非法命令名称 {funcName}", True)
        func = eval(funcName)
        func(*parList)
    else:
        # 没有输入命令
        exit("", True)


helpInfo = '''

beniutils task_create <target_path>
创建beniutils.task项目（如果不传入目标路径则在当前系统路径下进行）

beniutils task_build <target_path>
发布beniutils.task项目（如果不传入目标路径则在当前系统路径下进行）

'''

funcNameList = [
    "task_create",
    "task_build",
]


def task_create(targetPath: str = ""):
    targetPath = targetPath or os.getcwd()
    makeFolder(targetPath)
    workspaceFolder = makeTempWorkspace()
    try:
        taskCreateZipFile = getPath(os.path.dirname(__file__), "data/task_create.zip")
        zipFileExtract(taskCreateZipFile, workspaceFolder)
        for fileName in os.listdir(workspaceFolder):
            toFile = getPath(targetPath, fileName)
            if os.path.exists(toFile):
                raise Exception(f"创建失败，指定路径下已存在 {toFile}")
        for fileName in os.listdir(workspaceFolder):
            fromFile = getPath(workspaceFolder, fileName)
            toFile = getPath(targetPath, fileName)
            copy(fromFile, toFile)
        print("创建项目成功 " + targetPath)
    finally:
        remove(workspaceFolder)


def task_build(targetPath: str = ""):
    currentPath: str = ""
    workspaceFolder: str = ""
    try:
        currentPath = os.getcwd()
        targetPath = targetPath or currentPath
        workspaceFolder = makeTempWorkspace()
        ignoreList = ["main.py"]
        mainPyFile = getPath(targetPath, "project/src/main.py")
        if not os.path.isfile(mainPyFile):
            exit(f"发布失败，主文件不存在 {mainPyFile}")
        hiddenimports = [x[:-3] for x in os.listdir(os.path.dirname(mainPyFile)) if x.endswith(".py") and x not in ignoreList]
        name = "task"
        icon = getPath(workspaceFolder, "task.ico")
        pathex = getPath(targetPath, "project")
        taskBuildZipFile = getPath(os.path.dirname(__file__), "data/task_build.zip")
        zipFileExtract(taskBuildZipFile, workspaceFolder)
        taskSpecFile = getPath(workspaceFolder, "task.spec")
        taskSpecContent = readFile(taskSpecFile)
        taskSpecContent = taskSpecContent.replace("<<projectSrcPath>>", getPath(targetPath, "project/src"))
        taskSpecContent = taskSpecContent.replace("<<mainPyFile>>", mainPyFile)
        taskSpecContent = taskSpecContent.replace("<<pathex>>", pathex)
        taskSpecContent = taskSpecContent.replace("<<hiddenimports>>", ",".join([f'"{x}"' for x in hiddenimports]))
        taskSpecContent = taskSpecContent.replace("<<name>>", name)
        taskSpecContent = taskSpecContent.replace("<<icon>>", icon)
        print("------------------------------\n")
        print(taskSpecContent)
        print("------------------------------\n")
        writeFile(taskSpecFile, taskSpecContent)

        # import PyInstaller.__main__
        # sys.argv = ["", taskSpecFile]
        # PyInstaller.__main__.run() # pyinstaller main.py -F

        os.chdir(workspaceFolder)
        _, outBytes, errBytes = execute(f"pyinstaller {taskSpecFile}", ignoreError=True)

        outStr = decode(outBytes).replace("\r\n", "\n")
        errStr = decode(errBytes).replace("\r\n", "\n")
        executeLog = "\n".join([outStr, errStr])
        print(executeLog)

        fromExeFile = getPath(workspaceFolder, f"dist/{name}.exe")
        toExeFile = getPath(targetPath, "project/bin/" + os.path.basename(fromExeFile))
        if not os.path.exists(fromExeFile):
            exit("生成exe文件失败")
        remove(toExeFile)
        copy(fromExeFile, toExeFile)
    finally:
        if currentPath:
            os.chdir(currentPath)
        if workspaceFolder:
            remove(workspaceFolder)


def exit(errorMsg: str, isShowHelpInfo: bool = False):
    if errorMsg:
        print(errorMsg)
    if isShowHelpInfo:
        print(helpInfo)
    sys.exit(errorMsg and 1 or 0)
