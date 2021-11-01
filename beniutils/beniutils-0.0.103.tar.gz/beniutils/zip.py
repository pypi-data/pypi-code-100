import os
from typing import Callable, Optional, Union
from zipfile import ZIP_DEFLATED, ZipFile

from . import getAllFileAndFolderList, makeFolder


def zipFile(toFile: str, fileFolderOrAry: Union[str, list[str]], rename: Optional[Callable[[str], str]] = None):
    makeFolder(os.path.dirname(toFile))
    fileList: list[str] = []
    if type(fileFolderOrAry) is list:
        fileList = fileFolderOrAry
    elif type(fileFolderOrAry) is str:
        fileList = [fileFolderOrAry]
    rename = rename or (lambda x: os.path.basename(x))
    with ZipFile(toFile, 'w', ZIP_DEFLATED) as f:
        for file in sorted(fileList):
            fname = rename(file)
            f.write(file, fname)


def zipFileForFolder(toFile: str, folder: str, rename: Optional[Callable[[str], str]] = None, filterFun: Optional[Callable[[str], bool]] = None):
    if not folder.endswith(os.path.sep):
        folder += os.path.sep
    rename = rename or (lambda x: x[len(folder):])
    ary = getAllFileAndFolderList(folder)
    if filterFun:
        ary = list(filter(filterFun, ary))
    zipFile(toFile, ary, rename)


def zipFileExtract(file: str, toFolder: Optional[str] = None):
    toFolder = toFolder or os.path.dirname(file)
    with ZipFile(file) as f:
        for subFile in sorted(f.namelist()):
            try:
                # zipfile 代码中指定了cp437，这里会导致中文乱码
                encodeSubFile = subFile.encode('cp437').decode('gbk')
            except:
                encodeSubFile = subFile
            toFile = os.path.join(toFolder, encodeSubFile)
            toFile = toFile.replace('/', os.path.sep)
            f.extract(subFile, toFolder)
            # 处理压缩包中的中文文件名在windows下乱码
            if subFile != encodeSubFile:
                os.renames(os.path.join(toFolder, subFile), toFile)
