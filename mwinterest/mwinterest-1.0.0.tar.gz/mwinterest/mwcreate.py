import os
import os.path

def file():
    '''文件：目录&文件'''
    paths = []
    files = ["mp4", "txt", "docx", "xlsx"]
    movie = {
        "中国": ["胡歌", "霍哥", "丽姐", "璐姐", "喆姐"],
        "港台": ["星爷", "敏姐", "秋官"],
        "日本": ["海哥"]
    }
    #目录
    for key in movie:
        for value in movie[key]:
            path = r"电影\{0}\{1}".format(key, value)
            if not os.path.exists(path):
                os.makedirs(path)
                paths.append(path)
    #文件
    for x in paths:
        for y in files:
            filepath = r"{0}\{1}.{2}".format(x, x.split("\\")[-1], y)
            with open(filepath, "a+") as f:
                print(filepath)

def module():
    '''模块：包&源文件'''
    paths = []
    pkg = {
        "a": ["a{0}".format(x) for x in range(1, 11)],
        "b": ["b{0}".format(x) for x in range(1, 6)],
        "c": ["c{0}".format(x) for x in range(1, 4)]
    }
    #目录
    for key in pkg:
        for value in pkg[key]:
            #子包
            path1 = r"pkg\{0}\{1}".format(key, value)
            if not os.path.exists(path1):
                os.makedirs(path1)
                paths.append(path1)
            #init
            path2 = r"pkg\{0}".format(key)
            if not os.path.isfile(path2+"\\__init__.py"):
                with open(r"{0}\__init__.py".format(path2), "a+") as f:
                    f.write("print('{0}')".format(path2.split("\\")[-1]))
    #文件
    for x in paths:
        filestr = x.split("\\")[-1]
        #init
        filepath1 = r"{0}\__init__.py".format(x)
        with open(filepath1, "a+") as f:
            f.write("print('{0}')".format(filestr))
            print(filepath1)
        #模块
        for num in range(1, 4):
            filepath2 = r"{0}\m{1}_{2}.py".format(x, filestr, num)
            with open(filepath2, "a+") as f:
                f.write("print('{0}\\\\m{1}_{2}.py')\ndef m{1}_{2}fn():\n\tprint('m{1}_{2}fn()')".format(x.replace("\\", "\\\\"), filestr, num))
                print(filepath2)
